from flask import Flask
from threading import Thread
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Import handlers
from handlers.menu_handlers import menu_handler
from handlers.setup_handlers import setup_handler
from handlers.forward_handlers import forward_handler
from config import Config

# ==================== HEALTH CHECK SERVER ====================
app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot is running"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    server = Thread(target=run_flask, daemon=True)
    server.start()
    print("✅ Health check server started")

# Start health check server
keep_alive()

# ==================== BOT SETUP ====================
logging.basicConfig(
    format=Config.LOG_FORMAT,
    level=getattr(logging, Config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

class FastForwardBot:
    def __init__(self):
        self.token = Config.BOT_TOKEN
        if not self.token:
            raise ValueError("BOT_TOKEN not found")
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        
        # Button click handlers
        self.application.add_handler(CallbackQueryHandler(self.main_menu_click, pattern="^menu_"))
        self.application.add_handler(CallbackQueryHandler(self.forwarding_click, pattern="^forward_"))
        self.application.add_handler(CallbackQueryHandler(self.source_setup_click, pattern="^source_"))
        self.application.add_handler(CallbackQueryHandler(self.dest_setup_click, pattern="^dest_"))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.FORWARDED, self.handle_forwarded_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    # ==================== COMMAND HANDLERS ====================
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simple start command"""
        try:
            welcome_text = "Channel Forward Bot\n\nI help you move messages between channels quickly and safely."
            
            keyboard = [
                [InlineKeyboardButton("Set Source", callback_data="menu_setup_source")],
                [InlineKeyboardButton("Set Destination", callback_data="menu_setup_dest")],
                [InlineKeyboardButton("Start Forwarding", callback_data="menu_start_forward")],
                [InlineKeyboardButton("Status", callback_data="menu_status")],
                [InlineKeyboardButton("Help", callback_data="menu_help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
                
        except Exception as e:
            logger.error(f"Start error: {e}")
            await update.message.reply_text("Bot started. Use /help for instructions.")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simple help command"""
        help_text = """
Quick Guide:

1. Set Source Channel
2. Set Destination Channel  
3. Start Forwarding

I'll move messages automatically at optimal speed."""
        
        await update.message.reply_text(help_text)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simple status command"""
        status_text = f"""
System Status:

✅ Bot: Running
⚡ Speed: {Config.MAX_SPEED} msg/sec
🔄 Mode: Smart forwarding
📊 Ready: Yes

Use /start to begin."""
        
        await update.message.reply_text(status_text)
    
    # ==================== BUTTON HANDLERS ====================
    async def main_menu_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu button clicks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        try:
            if data == "menu_main":
                await menu_handler.show_main_menu(update, context)
            elif data == "menu_setup_source":
                await menu_handler.show_source_setup(update, context)
            elif data == "menu_setup_dest":
                await menu_handler.show_dest_setup(update, context)
            elif data == "menu_start_forward":
                await forward_handler.start_forwarding(update, context)
            elif data == "menu_status":
                await self.status_command(update, context)
            elif data == "menu_help":
                await self.help_command(update, context)
        except Exception as e:
            logger.error(f"Menu error: {e}")
            await query.message.reply_text("Please use /start to restart.")
    
    async def forwarding_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle forwarding control buttons"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        try:
            if data == "forward_start":
                await forward_handler.start_forwarding(update, context)
            elif data == "forward_pause":
                await forward_handler.pause_forwarding(update, context)
            elif data == "forward_stop":
                await forward_handler.stop_forwarding(update, context)
            elif data == "forward_stats":
                await query.answer("Status: Ready")
            elif data == "forward_resume":
                await query.answer("Ready to resume")
        except Exception as e:
            logger.error(f"Forward error: {e}")
            await query.answer("Action failed")
    
    async def source_setup_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle source channel setup"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        try:
            if data == "source_forward_msg":
                await query.edit_message_text("Forward a message from your source channel")
            elif data == "source_send_link":
                await query.edit_message_text("Send source channel link: @channel or t.me/link")
                context.user_data['awaiting_source_link'] = True
        except Exception as e:
            logger.error(f"Source error: {e}")
            await query.answer("Setup failed")
    
    async def dest_setup_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle destination channel setup"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        try:
            if data == "dest_forward_msg":
                await query.edit_message_text("Forward a message from your destination channel")
            elif data == "dest_send_link":
                await query.edit_message_text("Send destination channel link: @channel or t.me/link")
                context.user_data['awaiting_dest_link'] = True
        except Exception as e:
            logger.error(f"Dest error: {e}")
            await query.answer("Setup failed")
    
    # ==================== MESSAGE HANDLERS ====================
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        try:
            await setup_handler.handle_channel_link(update, context)
        except Exception as e:
            logger.error(f"Message error: {e}")
            await update.message.reply_text("Could not process message")
    
    async def handle_forwarded_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle forwarded messages"""
        try:
            user_id = update.message.from_user.id
            user_channels = await setup_handler.get_user_channels(user_id)
            
            if 'source' not in user_channels:
                await setup_handler.handle_source_forward(update, context)
            elif 'destination' not in user_channels:
                await setup_handler.handle_dest_forward(update, context)
            else:
                await update.message.reply_text("Channels set. Use /start to begin forwarding.")
        except Exception as e:
            logger.error(f"Forwarded error: {e}")
            await update.message.reply_text("Could not process forwarded message")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log errors without crashing"""
        logger.error(f"Error: {context.error}")
    
    def run(self):
        """Start the bot"""
        print("Bot starting...")
        self.application.run_polling()

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    try:
        if Config.validate_config():
            bot = FastForwardBot()
            bot.run()
        else:
            print("Config validation failed")
    except Exception as e:
        print(f"Bot failed: {e}")
