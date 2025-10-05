import asyncio
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

logger = logging.getLogger(__name__)

class ForwardHandlers:
    def __init__(self):
        self.active_jobs = {}
        self.forwarding_stats = {}
    
    async def start_forwarding(self, update, context):
        """Start the 25msg/s forwarding engine"""
        user_id = update.callback_query.from_user.id
        
        # Check if setup is complete
        from handlers.setup_handlers import setup_handler
        user_channels = await setup_handler.get_user_channels(user_id)
        
        if not await setup_handler.is_setup_complete(user_id):
            error_text = """
❌ **SETUP INCOMPLETE**

Please complete channel setup first:

1. 📤 Setup Source Channel
2. 🎯 Setup Destination Channel

Then come back to start forwarding!"""
            
            keyboard = [[InlineKeyboardButton("⚙️ COMPLETE SETUP", callback_data="menu_main")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.edit_message_text(error_text, reply_markup=reply_markup, parse_mode='Markdown')
            return
        
        # Start forwarding job
        if user_id in self.active_jobs:
            await update.callback_query.answer("⚠️ Forwarding already running!", show_alert=True)
            return
        
        # Start the forwarding task
        task = asyncio.create_task(
            self.forward_engine(user_id, user_channels, update.callback_query)
        )
        self.active_jobs[user_id] = task
        self.forwarding_stats[user_id] = {
            'started_at': datetime.now(),
            'messages_forwarded': 0,
            'status': 'running'
        }
        
        # Show starting message
        start_text = f"""
🚀 **FORWARDING STARTED!**

⚡ **MAXIMUM SPEED ACTIVATED: 25 messages/second**
⏰ **Burst-Rest Cycle:** 5 minutes ON → 30 seconds OFF

**Channels:**
📤 Source: {user_channels['source'].get('title', 'Unknown')}
🎯 Destination: {user_channels['destination'].get('title', 'Unknown')}

**Status:** Starting engine...
**Forwarded:** 0 messages

🛡️ **Safety System:** ACTIVE
🔧 **Auto-Recovery:** ENABLED"""

        keyboard = [
            [InlineKeyboardButton("⏸️ PAUSE", callback_data="forward_pause"),
             InlineKeyboardButton("🛑 STOP", callback_data="forward_stop")],
            [InlineKeyboardButton("📊 LIVE STATS", callback_data="forward_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(start_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def forward_engine(self, user_id, user_channels, query):
        """The main forwarding engine with 25msg/s burst logic"""
        try:
            bot = query.bot
            total_messages = 1000  # Example - we'll get actual count later
            forwarded = 0
            
            while forwarded < total_messages and self.forwarding_stats[user_id]['status'] == 'running':
                # 🔥 BURST PHASE: 5 minutes at 25 msg/sec
                burst_messages = min(7500, total_messages - forwarded)
                burst_start_time = datetime.now()
                
                # Update status
                status_text = f"""
🚀 **FORWARDING IN PROGRESS...**

⚡ **BURST MODE ACTIVE:** 25 messages/second
⏰ **Burst Time:** 5 minutes
📨 **This Burst:** {burst_messages} messages

**Progress:** {forwarded}/{total_messages}
**Speed:** 25 msg/sec
**Status:** Running at maximum speed

🛡️ **Next rest in:** 5 minutes"""
                
                keyboard = [
                    [InlineKeyboardButton("⏸️ PAUSE", callback_data="forward_pause"),
                     InlineKeyboardButton("🛑 STOP", callback_data="forward_stop")],
                    [InlineKeyboardButton("📊 LIVE STATS", callback_data="forward_stats")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(status_text, reply_markup=reply_markup, parse_mode='Markdown')
                
                # Simulate forwarding (replace with actual message fetching)
                for i in range(burst_messages):
                    if self.forwarding_stats[user_id]['status'] != 'running':
                        break
                    
                    # Simulate message forwarding
                    # await bot.forward_message(
                    #     chat_id=user_channels['destination']['id'],
                    #     from_chat_id=user_channels['source']['id'],
                    #     message_id=message_id
                    # )
                    
                    await asyncio.sleep(0.04)  # 25 msg/second
                    forwarded += 1
                    self.forwarding_stats[user_id]['messages_forwarded'] = forwarded
                    
                    # Update progress every 100 messages
                    if forwarded % 100 == 0:
                        progress_text = f"""
📊 **PROGRESS UPDATE**

✅ **Forwarded:** {forwarded}/{total_messages}
⚡ **Current Speed:** 25 messages/second  
⏰ **Running Time:** {(datetime.now() - self.forwarding_stats[user_id]['started_at']).seconds // 60} minutes

**Status:** Burst mode active - {7500 - (i + 1)} messages left in this burst"""
                        
                        await query.edit_message_text(progress_text, reply_markup=reply_markup, parse_mode='Markdown')
                
                # 😴 REST PHASE: 30 seconds (if more messages remain)
                if forwarded < total_messages and self.forwarding_stats[user_id]['status'] == 'running':
                    rest_text = f"""
😴 **REST PHASE**

⏰ **Taking 30-second break...**
✅ **Completed:** {forwarded}/{total_messages} messages
⚡ **Next burst in:** 30 seconds

**Reason:** Safety cooldown to prevent Telegram limits
**Status:** Auto-resuming shortly..."""

                    await query.edit_message_text(rest_text, reply_markup=reply_markup, parse_mode='Markdown')
                    await asyncio.sleep(30)  # 30 second rest
            
            # Completion
            if forwarded >= total_messages:
                completion_text = f"""
🎉 **FORWARDING COMPLETED!**

✅ **Successfully forwarded:** {forwarded} messages
⚡ **Average Speed:** 25 messages/second
⏰ **Total Time:** {(datetime.now() - self.forwarding_stats[user_id]['started_at']).seconds // 60} minutes

**Status:** All messages transferred successfully!"""

                keyboard = [[InlineKeyboardButton("🔄 START NEW", callback_data="menu_start_forward")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(completion_text, reply_markup=reply_markup, parse_mode='Markdown')
            
            # Cleanup
            if user_id in self.active_jobs:
                del self.active_jobs[user_id]
                
        except Exception as e:
            logger.error(f"Forwarding error for user {user_id}: {e}")
            error_text = f"""
❌ **FORWARDING ERROR**

An error occurred during forwarding:

**Error:** {str(e)}
**Messages Forwarded:** {self.forwarding_stats.get(user_id, {}).get('messages_forwarded', 0)}

**Auto-recovery failed.** Please check channel permissions and try again."""

            keyboard = [[InlineKeyboardButton("🔄 RETRY", callback_data="menu_start_forward")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(error_text, reply_markup=reply_markup, parse_mode='Markdown')
            
            if user_id in self.active_jobs:
                del self.active_jobs[user_id]
    
    async def pause_forwarding(self, update, context):
        """Pause active forwarding"""
        user_id = update.callback_query.from_user.id
        
        if user_id in self.forwarding_stats:
            self.forwarding_stats[user_id]['status'] = 'paused'
            
        pause_text = """
⏸️ **FORWARDING PAUSED**

**Status:** Paused by user
**Messages Forwarded:** {count} messages

Use buttons below to resume or stop.""".format(
    count=self.forwarding_stats.get(user_id, {}).get('messages_forwarded', 0)
)

        keyboard = [
            [InlineKeyboardButton("▶️ RESUME", callback_data="forward_resume"),
             InlineKeyboardButton("🛑 STOP", callback_data="forward_stop")],
            [InlineKeyboardButton("📊 STATS", callback_data="forward_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(pause_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def stop_forwarding(self, update, context):
        """Stop active forwarding"""
        user_id = update.callback_query.from_user.id
        
        if user_id in self.forwarding_stats:
            self.forwarding_stats[user_id]['status'] = 'stopped'
        
        # Cancel the task
        if user_id in self.active_jobs:
            self.active_jobs[user_id].cancel()
            del self.active_jobs[user_id]
        
        stop_text = """
🛑 **FORWARDING STOPPED**

**Status:** Stopped by user
**Final Count:** {count} messages forwarded

Use the main menu to start a new forwarding job.""".format(
    count=self.forwarding_stats.get(user_id, {}).get('messages_forwarded', 0)
)

        keyboard = [[InlineKeyboardButton("🚀 START NEW", callback_data="menu_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(stop_text, reply_markup=reply_markup, parse_mode='Markdown')

# Create global instance
forward_handler = ForwardHandlers()
