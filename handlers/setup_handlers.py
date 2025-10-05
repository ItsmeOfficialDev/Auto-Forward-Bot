from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import re

logger = logging.getLogger(__name__)

class SetupHandlers:
    def __init__(self):
        self.user_channels = {}  # Temporary storage
    
    async def handle_source_forward(self, update, context):
        """Handle forwarded message from source channel"""
        if not update.message.forward_from_chat:
            await update.message.reply_text(
                "❌ That doesn't look like a forwarded channel message. "
                "Please forward a message from your source channel.",
                parse_mode='Markdown'
            )
            return
        
        chat = update.message.forward_from_chat
        user_id = update.message.from_user.id
        
        if chat.type != "channel":
            await update.message.reply_text(
                "❌ That's not a channel message. Please forward from a **channel**.",
                parse_mode='Markdown'
            )
            return
        
        # Store source channel info
        if user_id not in self.user_channels:
            self.user_channels[user_id] = {}
        
        self.user_channels[user_id]['source'] = {
            'id': chat.id,
            'username': chat.username,
            'title': chat.title,
            'type': 'private' if not chat.username else 'public'
        }
        
        success_text = f"""
✅ **SOURCE CHANNEL SETUP COMPLETE!**

📝 **Channel Details:**
• **Name:** {chat.title}
• **Type:** {'Public' if chat.username else 'Private'}
• **Username:** @{chat.username if chat.username else 'N/A'}

**Next Step:** Setup destination channel!"""

        keyboard = [[InlineKeyboardButton("🎯 SETUP DESTINATION", callback_data="menu_setup_dest")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_dest_forward(self, update, context):
        """Handle forwarded message from destination channel"""
        if not update.message.forward_from_chat:
            await update.message.reply_text(
                "❌ That doesn't look like a forwarded channel message. "
                "Please forward a message from your destination channel.",
                parse_mode='Markdown'
            )
            return
        
        chat = update.message.forward_from_chat
        user_id = update.message.from_user.id
        
        if chat.type != "channel":
            await update.message.reply_text(
                "❌ That's not a channel message. Please forward from a **channel**.",
                parse_mode='Markdown'
            )
            return
        
        # Store destination channel info
        if user_id not in self.user_channels:
            self.user_channels[user_id] = {}
        
        self.user_channels[user_id]['destination'] = {
            'id': chat.id,
            'username': chat.username,
            'title': chat.title,
            'type': 'private' if not chat.username else 'public'
        }
        
        success_text = f"""
✅ **DESTINATION CHANNEL SETUP COMPLETE!**

📝 **Channel Details:**
• **Name:** {chat.title}
• **Type:** {'Public' if chat.username else 'Private'}
• **Username:** @{chat.username if chat.username else 'N/A'}

**🚀 Ready to start forwarding!**"""

        keyboard = [[InlineKeyboardButton("🚀 START FORWARDING", callback_data="menu_start_forward")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_channel_link(self, update, context):
        """Handle channel links (@username or t.me links)"""
        text = update.message.text
        user_id = update.message.from_user.id
        
        # Extract channel username from different formats
        channel_username = self.extract_channel_username(text)
        
        if not channel_username:
            await update.message.reply_text(
                "❌ Couldn't detect a valid channel link. "
                "Please send in format: @channel_username or https://t.me/channel_username",
                parse_mode='Markdown'
            )
            return
        
        # Store channel info (we'll verify access later)
        if user_id not in self.user_channels:
            self.user_channels[user_id] = {}
        
        # Determine if this is source or destination based on context
        if 'awaiting_source_link' in context.user_data:
            self.user_channels[user_id]['source'] = {
                'username': channel_username,
                'type': 'public'  # Assume public for links
            }
            del context.user_data['awaiting_source_link']
            success_text = f"✅ Source channel set: @{channel_username}"
        elif 'awaiting_dest_link' in context.user_data:
            self.user_channels[user_id]['destination'] = {
                'username': channel_username,
                'type': 'public'  # Assume public for links
            }
            del context.user_data['awaiting_dest_link']
            success_text = f"✅ Destination channel set: @{channel_username}"
        else:
            await update.message.reply_text(
                "❌ Please use the setup buttons first to specify if this is source or destination.",
                parse_mode='Markdown'
            )
            return
        
        keyboard = [[InlineKeyboardButton("🚀 CONTINUE SETUP", callback_data="menu_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(success_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def extract_channel_username(self, text):
        """Extract channel username from various formats"""
        # Handle @username format
        if text.startswith('@'):
            return text[1:]
        
        # Handle t.me/username format
        tme_match = re.search(r't\.me/([a-zA-Z0-9_]+)', text)
        if tme_match:
            return tme_match.group(1)
        
        # Handle https://t.me/username format
        https_match = re.search(r'https?://t\.me/([a-zA-Z0-9_]+)', text)
        if https_match:
            return https_match.group(1)
        
        return None
    
    async def get_user_channels(self, user_id):
        """Get channels for a user"""
        return self.user_channels.get(user_id, {})
    
    async def is_setup_complete(self, user_id):
        """Check if user has both channels setup"""
        channels = self.user_channels.get(user_id, {})
        return 'source' in channels and 'destination' in channels

# Create global instance
setup_handler = SetupHandlers()
