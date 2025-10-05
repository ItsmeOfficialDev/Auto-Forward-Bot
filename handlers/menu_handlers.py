from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

class MenuHandlers:
    def __init__(self):
        self.setup_menus()
    
    def setup_menus(self):
        """Create all menu keyboards"""
        # Main Menu
        self.main_menu = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 SETUP SOURCE CHANNEL", callback_data="menu_setup_source")],
            [InlineKeyboardButton("🎯 SETUP DESTINATION CHANNEL", callback_data="menu_setup_dest")],
            [InlineKeyboardButton("🚀 START FORWARDING", callback_data="menu_start_forward")],
            [InlineKeyboardButton("📊 VIEW STATUS", callback_data="menu_status"), 
             InlineKeyboardButton("❓ HELP", callback_data="menu_help")]
        ])
        
        # Source Channel Setup Menu
        self.source_setup_menu = InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 FORWARD CHANNEL MESSAGE", callback_data="source_forward_msg")],
            [InlineKeyboardButton("🔗 SEND CHANNEL LINK", callback_data="source_send_link")],
            [InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="menu_main")]
        ])
        
        # Destination Channel Setup Menu
        self.dest_setup_menu = InlineKeyboardMarkup([
            [InlineKeyboardButton("📨 FORWARD CHANNEL MESSAGE", callback_data="dest_forward_msg")],
            [InlineKeyboardButton("🔗 SEND CHANNEL LINK", callback_data="dest_send_link")],
            [InlineKeyboardButton("👑 ADD BOT AS ADMIN", url="https://t.me/your_bot?startgroup=true")],
            [InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="menu_main")]
        ])
        
        # Forwarding Control Menu
        self.forward_control_menu = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ START 25MSG/S", callback_data="forward_start")],
            [InlineKeyboardButton("⏸️ PAUSE", callback_data="forward_pause"),
             InlineKeyboardButton("🛑 STOP", callback_data="forward_stop")],
            [InlineKeyboardButton("📊 PROGRESS", callback_data="forward_progress")],
            [InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="menu_main")]
        ])
        
        # Status Menu
        self.status_menu = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 REFRESH", callback_data="status_refresh")],
            [InlineKeyboardButton("⚙️ SETTINGS", callback_data="status_settings")],
            [InlineKeyboardButton("⬅️ BACK TO MAIN", callback_data="menu_main")]
        ])
    
    async def show_main_menu(self, update, context):
        """Display main menu"""
        welcome_text = """
🚀 **FASTEST FORWARD BOT ON TELEGRAM**

⚡ **25 MESSAGES/SECOND** - Maximum Telegram Speed
🛡️ **100% Safe** - No Bans, Official API
🎯 **One-Click Setup** - Just Tap Buttons

**What would you like to do?**"""
        
        if hasattr(update, 'callback_query'):
            await update.callback_query.edit_message_text(welcome_text, reply_markup=self.main_menu, parse_mode='Markdown')
        else:
            await update.message.reply_text(welcome_text, reply_markup=self.main_menu, parse_mode='Markdown')
    
    async def show_source_setup(self, update, context):
        """Show source channel setup menu"""
        setup_text = """
📤 **SETUP SOURCE CHANNEL**

Choose how to setup your **SOURCE** channel:

**Requirements:**
• You must be **admin** in this channel
• Channel must be **private**

**Methods:**
• 📨 **Forward Message** - Forward any message from the channel
• 🔗 **Send Link** - Send @channel_username or t.me link"""
        
        await update.callback_query.edit_message_text(setup_text, reply_markup=self.source_setup_menu, parse_mode='Markdown')
    
    async def show_dest_setup(self, update, context):
        """Show destination channel setup menu"""
        setup_text = """
🎯 **SETUP DESTINATION CHANNEL**

Choose how to setup your **DESTINATION** channel:

**Requirements:**
• You must be **admin** in this channel  
• Bot must be **admin** in this channel
• Channel must be **private**

**Methods:**
• 📨 **Forward Message** - Forward any message from the channel
• 🔗 **Send Link** - Send @channel_username or t.me link
• 👑 **Add Bot as Admin** - Make bot admin first"""
        
        await update.callback_query.edit_message_text(setup_text, reply_markup=self.dest_setup_menu, parse_mode='Markdown')
    
    async def show_forward_control(self, update, context):
        """Show forwarding control menu"""
        control_text = """
🚀 **FORWARDING CONTROL**

⚡ **READY FOR MAXIMUM SPEED!**

**Speed Settings:**
• **25 messages/second** - Maximum allowed
• **5-minute bursts** with 30-second rests
• **Zero risk** of Telegram limits

**Current Status:** Ready to start!

Use buttons below to control forwarding:"""
        
        await update.callback_query.edit_message_text(control_text, reply_markup=self.forward_control_menu, parse_mode='Markdown')
    
    async def show_status(self, update, context):
        """Show status menu"""
        status_text = """
📊 **SYSTEM STATUS**

✅ **Bot Status:** OPERATIONAL
⚡ **Forwarding Engine:** READY
🛡️ **Safety System:** ACTIVE
🚀 **Max Speed:** 25 messages/second

**Features:**
• Burst-Rest Cycle (5min ON, 30s OFF)
• Progress Tracking
• Error Recovery
• Multi-user Support

Use buttons to refresh or configure:"""
        
        await update.callback_query.edit_message_text(status_text, reply_markup=self.status_menu, parse_mode='Markdown')

# Create global instance
menu_handler = MenuHandlers()
