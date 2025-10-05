# 🚀 Telegram Fast Forward Bot

**The FASTEST Channel Forwarding Bot on Telegram - 25 Messages/Second!** ⚡

![Bot Speed](https://img.shields.io/badge/Speed-25_msg%2Fsec-green)
![Safety](https://img.shields.io/badge/Safety-100%25_Compliant-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Telegram-blue)

## 🌟 Features

### ⚡ **Blazing Fast Speed**
- **25 messages/second** - Maximum allowed by Telegram API
- **7,500 messages per 5-minute burst**
- **Smart rest periods** to avoid limits
- **Zero risk of bans** - completely safe

### 🎯 **Professional Interface**
- **100% button-based** - No commands to remember
- **Live progress tracking** with real-time updates
- **Pause/Resume/Stop** controls
- **Auto-error recovery** system

### 🛡️ **Enterprise Grade Safety**
- **Pure Bot API** - No userbot risks
- **Burst-Rest Cycle** - 5 minutes ON, 30 seconds OFF
- **Permission verification** before starting
- **Multi-user support** with isolation

## 📸 Bot Preview
🔒 FAST FORWARD BOT - MAIN MENU
┌─────────────────────────────────────┐
│ 🤖 Welcome! Tap buttons to setup:   │
│                                     │
│ [📤 SETUP SOURCE CHANNEL]           │
│ [🎯 SETUP DESTINATION CHANNEL]      │
│ [🚀 START FORWARDING]               │
│ [📊 VIEW STATUS]                    │
│ [❓ GET HELP]                       │
└────────────────────────────

## 🚀 Quick Start

### Method 1: Use Our Hosted Bot (Easy)
**Coming Soon!** - Hosted version will be available soon

### Method 2: Deploy Your Own Instance (Recommended)

#### 📋 Prerequisites:
- Python 3.8+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- [Koyeb](https://www.koyeb.com/) account (free tier available)

#### 🛠️ Deployment Steps:

1. **⭐ Fork This Repository**
   - Click the **"Fork"** button at the top right of this page
   - This creates your own copy of the code

2. **🤖 Get Bot Token:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Save your bot token (looks like: `123456:ABCdefGHIjkl`)

3. **☁️ Deploy to Koyeb:**
   - Go to [Koyeb.com](https://www.koyeb.com/)
   - Click **"Create App"**
   - Connect your GitHub account
   - Select your forked repository
   - Add environment variable:
     - **Name:** `BOT_TOKEN`
     - **Value:** `your_bot_token_here` (paste your token)
   - Click **"Deploy"**

4. **🎉 Start Using Your Bot:**
   - Go to your bot on Telegram: `t.me/YourBotUsername`
   - Send `/start`
   - Follow the button instructions!

## 💡 How It Works

### 🔄 Setup Process:
1. **Setup Source Channel** - Where to read messages from
2. **Setup Destination Channel** - Where to send messages to
3. **Start Forwarding** - Watch the magic happen!

### ⚡ Speed System:
- **25 messages/second** during active bursts
- **5 minutes** of maximum speed forwarding
- **30 seconds** of rest to prevent limits
- **Auto-resume** after rest periods

## 🛡️ Safety Features

- ✅ **Official Telegram Bot API** - No risky userbots
- ✅ **Automatic rate limiting** - Never get banned
- ✅ **Permission checks** - Verify admin access
- ✅ **Error recovery** - Resume if interrupted
- ✅ **Progress saving** - Continue where you left off

## 📁 File Structure
telegram-fast-forwarder/
├── main.py                 # Main bot application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
└── handlers/             # Bot functionality modules
    ├── menu_handlers.py     # Button interfaces
    ├── setup_handlers.py    # Channel setup
    └── forward_handlers.py  # 25msg/s engine
    
## 🐛 Troubleshooting

### Common Issues:

**❌ Bot not starting:**
- Check if BOT_TOKEN is correctly set in Koyeb
- Ensure all files are uploaded to GitHub

**❌ Can't forward messages:**
- Make sure bot is admin in destination channel
- Verify you're admin in source channel
- Check channel privacy settings

**❌ Speed too slow:**
- Bot automatically adjusts speed for safety
- 25msg/s is maximum - be patient for large channels

## 🤝 Contributing

**Want to improve this bot?** 
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⭐ Support

If you like this project, please give it a star! ⭐

**Happy Forwarding!** 🚀
