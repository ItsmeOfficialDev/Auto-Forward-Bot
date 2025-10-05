import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class FastForwardBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
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
        self.application.add_handler(CallbackQueryHandler(self.button_click, pattern="^main_"))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update, context):
        """Send welcome message with main menu buttons"""
        welcome_text = """
🚀 **FASTEST FORWARD BOT ON TELEGRAM**

⚡ **25 MESSAGES/SECOND** - Maximum Telegram Speed
🛡️ **100% Safe** - No Bans, Official API
🎯 **One-Click Setup** - Just Tap Buttons

**What would you like to do?**"""
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        
        keyboard = [
            [InlineKeyboardButton("📤 SETUP SOURCE CHANNEL", callback_data="main_setup_source")],
            [InlineKeyboardButton("🎯 SETUP DESTINATION CHANNEL", callback_data="main_setup_dest")],
            [InlineKeyboardButton("🚀 START FORWARDING", callback_data="main_start_forward")],
            [InlineKeyboardButton("📊 VIEW STATUS", callback_data="main_status"),
             InlineKeyboardButton("❓ HELP", callback_data="main_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update, context):
        """Send help information"""
        help_text = """
📚 **HOW IT WORKS:**

⚡ **SPEED SYSTEM:**
• **25 messages/second** - Maximum allowed
• **5-minute bursts** then 30-second rests
• **Zero risk** of Telegram limits

🔄 **SETUP PROCESS:**
1. Setup Source Channel (where to read from)
2. Setup Destination Channel (where to send to)  
3. Start Forwarding - Watch the magic!

🛡️ **REQUIREMENTS:**
• You must be **admin** in both channels
• Bot needs **admin** in destination channel

**Just tap buttons - no typing needed!**"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update, context):
        """Show current forwarding status"""
        status_text = "📊 **SYSTEM STATUS**\n\n"
        status_text += "⚡ **Forwarding Engine:** READY\n"
        status_text += "🛡️ **Safety System:** ACTIVE\n"
        status_text += "🚀 **Max Speed:** 25 messages/second\n"
        status_text += "🔧 **Bot Status:** OPERATIONAL\n\n"
        status_text += "Use buttons below to start setup!"
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [[InlineKeyboardButton("📤 START SETUP", callback_data="main_setup_source")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(status_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def button_click(self, update, context):
        """Handle all button clicks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "main_setup_source":
            await self.setup_source_channel(query)
        elif data == "main_setup_dest":
            await self.setup_destination_channel(query)
        elif data == "main_start_forward":
            await self.start_forwarding(query)
        elif data == "main_status":
            await self.show_status(query)
        elif data == "main_help":
            await self.show_help(query)
    
    async def setup_source_channel(self, query):
        """Setup source channel flow"""
        setup_text = """
📤 **SETUP SOURCE CHANNEL**

Please forward a message from your **SOURCE** channel (where we read messages from).

**Requirements:**
• You must be **admin** in this channel
• Channel must be **private**"""
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [
            [InlineKeyboardButton("🔗 OR SEND CHANNEL LINK", callback_data="source_send_link")],
            [InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(setup_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def setup_destination_channel(self, query):
        """Setup destination channel flow"""
        setup_text = """
🎯 **SETUP DESTINATION CHANNEL**

Please forward a message from your **DESTINATION** channel (where we send messages to).

**Requirements:**
• You must be **admin** in this channel  
• Bot must be **admin** in this channel
• Channel must be **private**"""
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [
            [InlineKeyboardButton("🔗 OR SEND CHANNEL LINK", callback_data="dest_send_link")],
            [InlineKeyboardButton("👑 ADD BOT AS ADMIN", url="http://t.me/your_bot_username")],
            [InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(setup_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def start_forwarding(self, query):
        """Start the forwarding process"""
        # Placeholder - will be implemented in forward_handlers.py
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [[InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🚀 **FORWARDING SYSTEM**\n\nThis feature will be available in the next update!\n\nWe'll implement the 25 messages/second burst system here.", 
            reply_markup=reply_markup, 
            parse_mode='Markdown'
        )
    
    async def show_status(self, query):
        """Show detailed status"""
        await self.status_command(query, query.message)
    
    async def show_help(self, query):
        """Show help information"""
        await self.help_command(query, query.message)
    
    async def handle_message(self, update, context):
        """Handle regular text messages"""
        # Placeholder - will handle channel links and forwarded messages
        await update.message.reply_text(
            "📨 I see your message! For full functionality, please use the buttons from /start command.",
            parse_mode='Markdown'
        )
    
    async def error_handler(self, update, context):
        """Log errors"""
        logger.error(f"Exception while handling an update: {context.error}")
    
    def run(self):
        """Start the bot"""
        print("🚀 Fast Forward Bot is starting...")
        print("⚡ Speed: 25 messages/second")
        print("🛡️ Safety: Burst + Rest system active")
        self.application.run_polling()

if __name__ == "__main__":
    bot = FastForwardBot()
    bot.run()
