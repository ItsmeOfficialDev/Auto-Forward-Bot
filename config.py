import os

class Config:
    # Bot Token from environment variable
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Speed Configuration - 25 MESSAGES/SECOND 🚀
    MAX_SPEED = 25  # messages per second
    BURST_DURATION = 300  # 5 minutes in seconds
    REST_DURATION = 30  # 30 seconds rest
    
    # Safety Limits
    MAX_MESSAGES_PER_JOB = 100000
    MAX_JOBS_PER_USER = 3
    
    # Forwarding Settings
    DEFAULT_DELAY = 0.04  # 25 msg/second (1/25 = 0.04)
    PROGRESS_UPDATE_INTERVAL = 100  # Update every 100 messages
    
    # Channel Settings
    ALLOW_PUBLIC_CHANNELS = True
    ALLOW_PRIVATE_CHANNELS = True
    REQUIRED_DESTINATION_PERMISSIONS = ["can_post_messages", "can_edit_messages"]
    
    # Database Settings (we'll use simple dict for now)
    USE_DATABASE = False  # Set to True for production
    
    # Logging Configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Bot Information
    BOT_USERNAME = "@Speed_Fast_Forward_bot"  # Update with your bot username
    SUPPORT_CHAT = "https://t.me/Oggybotz"  # Update if you have support channel
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configurations are set"""
        if not cls.BOT_TOKEN:
            print("❌ BOT_TOKEN is not set in environment variables")
            return False
        
        if cls.MAX_SPEED > 30:
            print("❌ MAX_SPEED cannot exceed 30 messages/second")
            return False
        
        required_vars = {
            'BOT_TOKEN': cls.BOT_TOKEN,
            'MAX_SPEED': cls.MAX_SPEED,
            'BURST_DURATION': cls.BURST_DURATION,
            'REST_DURATION': cls.REST_DURATION
        }
        
        for var_name, var_value in required_vars.items():
            if var_value is None:
                print(f"❌ Required configuration {var_name} is not set")
                return False
        
        print("✅ All configurations validated successfully!")
        print(f"🚀 Bot configured for {cls.MAX_SPEED} messages/second")
        print(f"⏰ Burst-Rest Cycle: {cls.BURST_DURATION}s ON → {cls.REST_DURATION}s OFF")
        return True

# Validate configuration but don't exit if fails
try:
    Config.validate_config()
except Exception as e:
    print(f"⚠️ Configuration check had issues: {e}")
    print("🔧 Continuing anyway...")
