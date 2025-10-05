import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import our handlers
from handlers.menu_handlers import menu_handler
from handlers.setup_handlers import setup_handler
from handlers.forward_handlers import forward_handler
from config import Config

# Load environment variables
load_dotenv()

# Configure logging
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
        
        # Button click handlers - MAIN MENU
        self.application.add_handler(CallbackQueryHandler(self.main_menu_click, pattern="^menu_"))
        
        # Button click handlers - FORWARDING
        self.application.add_handler(CallbackQueryHandler(self.forwarding_click, pattern="^forward_"))
        
        # Button click handlers - SOURCE SETUP
        self.application.add_handler(CallbackQueryHandler(self.source_setup_click, pattern="^source_"))
        
        # Button click handlers - DESTINATION SETUP
        self.application.add_handler(CallbackQueryHandler(self.dest_setup_click, pattern="^dest_"))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.FORWARDED, self.handle_forwarded_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    # MAIN MENU COMMANDS
    async def start_command(self, update, context):
        await menu_handler.show_main_menu(update, context)
    
    async def help_command(self, update, context):
        help_text = """
📚 **FAST FORWARD BOT - COMPLETE GUIDE**

⚡ **SPEED SYSTEM:**
• **25 messages/second** - Maximum Telegram allows
• **5-minute bursts** then **30-second rests**
• **Zero risk** of bans or limits

🔄 **HOW TO USE:**
1. **Setup Source Channel** (where to read from)
2. **Setup Destination Channel** (where to send to)
3. **Start Forwarding** - Watch the magic!

🛡️ **REQUIREMENTS:**
• You must be **admin** in both channels
• Bot needs **admin** in destination channel

🎯 **FEATURES:**
• One-click button interface
• Live progress tracking
• Pause/Resume/Stop controls
• Error recovery system

**Just tap buttons - it's that easy!**"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update, context):
        await menu_handler.show_status(update, context)
    
    # BUTTON CLICK HANDLERS
    async def main_menu_click(self, update, context):
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
            await menu_handler.show_status(update, context)
        elif data == "menu_help":
            await self.help_command(update, context)
    
    async def forwarding_click(self, update, context):
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
            await query.answer("📊 Stats feature coming soon!", show_alert=True)
        elif data == "forward_resume":
            await query.answer("▶️ Resume feature coming soon!", show_alert=True)
    
    async def source_setup_click(self, update, context):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "source_forward_msg":
            await query.edit_message_text(
                "📨 **Please forward any message from your SOURCE channel now...**\n\n"
                "I'll automatically detect the channel and save it.",
                parse_mode='Markdown'
            )
        elif data == "source_send_link":
            await query.edit_message_text(
                "🔗 **Please send your SOURCE channel link:**\n\n"
                "Format: @channel_username or https://t.me/channel_username",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_source_link'] = True
    
    async def dest_setup_click(self, update, context):
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "dest_forward_msg":
            await query.edit_message_text(
                "📨 **Please forward any message from your DESTINATION channel now...**\n\n"
                "I'll automatically detect the channel and save it.",
                parse_mode='Markdown'
            )
        elif data == "dest_send_link":
            await query.edit_message_text(
                "🔗 **Please send your DESTINATION channel link:**\n\n"
                "Format: @channel_username or https://t.me/channel_username",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_dest_link'] = True
    
    # MESSAGE HANDLERS
    async def handle_message(self, update, context):
        """Handle regular text messages (channel links)"""
        await setup_handler.handle_channel_link(update, context)
    
    async def handle_forwarded_message(self, update, context):
        """Handle forwarded messages from channels"""
        user_id = update.message.from_user.id
        user_channels = await setup_handler.get_user_channels(user_id)
        
        if 'source' not in user_channels:
            await setup_handler.handle_source_forward(update, context)
        elif 'destination' not in user_channels:
            await setup_handler.handle_dest_forward(update, context)
        else:
            await update.message.reply_text(
                "✅ Both channels already setup! Use the buttons from /start to begin forwarding.",
                parse_mode='Markdown'
            )
    
    async def error_handler(self, update, context):
        """Log errors"""
        logger.error(f"Exception while handling an update: {context.error}")
    
    def run(self):
        """Start the bot"""
        print("🚀 Fast Forward Bot is starting...")
        print(f"⚡ Speed: {Config.MAX_SPEED} messages/second")
        print(f"🛡️ Safety: {Config.BURST_DURATION}s ON + {Config.REST_DURATION}s OFF")
        print("✅ All systems operational!")
        self.application.run_polling()

if __name__ == "__main__":
    bot = FastForwardBot()
    bot.run()
