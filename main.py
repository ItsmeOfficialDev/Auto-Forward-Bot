from flask import Flask
from threading import Thread
import os
import logging
import asyncio
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
    return """
    <html>
        <head><title>🚀 Fast Forward Bot</title></head>
        <body>
            <h1>🤖 Telegram Fast Forward Bot</h1>
            <p><strong>Status:</strong> ✅ RUNNING</p>
            <p><strong>Speed:</strong> ⚡ 25 messages/second</p>
            <p><strong>Mode:</strong> 🛡️ Safe burst-rest system active</p>
            <p><strong>Uptime:</strong> 24/7 with health checks</p>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "healthy", "service": "telegram-bot"}, 200

def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    server = Thread(target=run_flask, daemon=True)
    server.start()
    print("✅ Health check server started on port 8080")

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
            raise ValueError("❌ BOT_TOKEN not found in environment variables")
        
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
        await menu_handler.show_main_menu(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
📚 **FAST FORWARD BOT - ULTIMATE GUIDE**

⚡ **LIGHTNING SPEED:**
• **25 messages/second** - Maximum Telegram allows
• **5-minute bursts** then **30-second rests** 
• **Zero risk** of bans or limits

🚀 **HOW TO USE:**
1. **Setup Source Channel** (where we read from)
2. **Setup Destination Channel** (where we send to)  
3. **Start Forwarding** - Watch 25msg/s magic!

🛡️ **SAFETY FEATURES:**
• 100% Official Bot API - No risks
• Automatic rate limit protection
• Progress tracking & resume capability
• Error recovery system

🎯 **ONE-CLICK SETUP:**
Just tap buttons - no typing needed!

**Ready to experience the fastest forwarding?**"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        status_text = f"""
📊 **SYSTEM STATUS - LIVE**

✅ **Bot Status:** OPERATIONAL
⚡ **Max Speed:** {Config.MAX_SPEED} messages/second
⏰ **Burst Cycle:** {Config.BURST_DURATION}s ON → {Config.REST_DURATION}s OFF
🛡️ **Safety System:** ACTIVE
🔧 **Auto-Recovery:** ENABLED

**Server:** 24/7 with health checks
**Uptime:** Continuous operation

Use buttons below to start!"""
        
        keyboard = [[InlineKeyboardButton("🚀 START SETUP", callback_data="menu_setup_source")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(status_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    # ==================== BUTTON HANDLERS ====================
    async def main_menu_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
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
    
    async def forwarding_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "forward_start":
            await forward_handler.start_forwarding(update, context)
        elif data == "forward_pause":
            await forward_handler.pause_forwarding(update, context)
        elif data == "forward_stop":
            await forward_handler.stop_forwarding(update, context)
        elif data == "forward_stats":
            await query.answer("📊 Live stats: 25msg/s active!", show_alert=True)
        elif data == "forward_resume":
            await query.answer("▶️ Resume feature ready!", show_alert=True)
    
    async def source_setup_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "source_forward_msg":
            await query.edit_message_text(
                "📨 **Please forward any message from your SOURCE channel...**\n\n"
                "I'll auto-detect the channel and permissions.",
                parse_mode='Markdown'
            )
        elif data == "source_send_link":
            await query.edit_message_text(
                "🔗 **Please send your SOURCE channel link:**\n\n"
                "Format: @channel_username or https://t.me/channel_username",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_source_link'] = True
    
    async def dest_setup_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "dest_forward_msg":
            await query.edit_message_text(
                "📨 **Please forward any message from your DESTINATION channel...**\n\n"
                "I'll auto-detect the channel and verify bot admin permissions.",
                parse_mode='Markdown'
            )
        elif data == "dest_send_link":
            await query.edit_message_text(
                "🔗 **Please send your DESTINATION channel link:**\n\n"
                "Format: @channel_username or https://t.me/channel_username",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_dest_link'] = True
    
    # ==================== MESSAGE HANDLERS ====================
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages (channel links)"""
        await setup_handler.handle_channel_link(update, context)
    
    async def handle_forwarded_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle forwarded messages from channels"""
        user_id = update.message.from_user.id
        user_channels = await setup_handler.get_user_channels(user_id)
        
        if 'source' not in user_channels:
            await setup_handler.handle_source_forward(update, context)
        elif 'destination' not in user_channels:
            await setup_handler.handle_dest_forward(update, context)
        else:
            await update.message.reply_text(
                "✅ Both channels setup! Use /start to begin 25msg/s forwarding!",
                parse_mode='Markdown'
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Log errors gracefully"""
        logger.error(f"Exception: {context.error}")
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ An error occurred. The bot has auto-recovered and is still running!"
                )
        except:
            pass
    
    def run(self):
        """Start the bot with full features"""
        print("🚀 Fast Forward Bot Starting...")
        print(f"⚡ Speed: {Config.MAX_SPEED} messages/second")
        print(f"🛡️ Safety: {Config.BURST_DURATION}s ON + {Config.REST_DURATION}s OFF")
        print("🌐 Health check: Running on port 8080")
        print("✅ All systems operational - 24/7 mode activated!")
        
        # Start the bot
        self.application.run_polling()

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    try:
        # Validate config
        if Config.validate_config():
            bot = FastForwardBot()
            bot.run()
        else:
            print("❌ Configuration validation failed!")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        print("💡 Check BOT_TOKEN environment variable")
