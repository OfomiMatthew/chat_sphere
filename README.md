# 🟢 ChatSphere - Splinter Cell Edition

A fully-featured, AI-powered chat application built with Flask and styled with a sleek Splinter Cell-inspired dark green/black theme using TailwindCSS. Now with advanced AI capabilities powered by Groq API!

![Splinter Cell Theme](https://img.shields.io/badge/Theme-Splinter%20Cell-00ff41?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.0.0-00ff41?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.9%2B-00ff41?style=for-the-badge&logo=python)
![AI Powered](https://img.shields.io/badge/AI-Groq%20Powered-00ff41?style=for-the-badge&logo=ai)

## ✨ Features

### 🤖 AI Features (NEW!)

- **AI Chat Assistant** - Chat with an intelligent AI bot powered by Llama 3.3 70B
- **Smart Reply Suggestions** - Get contextual reply suggestions with one click
- **Message Translation** - Translate messages to 10+ languages instantly
- **Message Enhancement** - Improve message tone (professional, casual, friendly, formal, concise)
- **Voice Transcription** - Convert voice messages to text using Whisper AI
- **Content Moderation** - AI-powered safety checks for inappropriate content
- **Sentiment Analysis** - Understand emotional tone of messages
- **Conversation Summarization** - Get AI-generated summaries of long chats
- **Smart Search** - Semantic search through messages using natural language
- **Autocomplete** - AI-powered text completion suggestions

📖 **[Read Full AI Features Documentation →](AI_FEATURES.md)**

### 💬 Real-Time Messaging

- **Instant messaging** with Socket.IO real-time updates
- **Read receipts** with double-check marks
- **Typing indicators** to show when someone is typing
- **Last seen** and online/offline status
- **Message reactions** with emoji support
- **Reply to messages** functionality
- **Delete messages** for yourself

### 👥 Group Chats

- **Create groups** with multiple members
- **Group messaging** with member names displayed
- **Add/remove members** (group admin features)
- **Group profile pictures** and descriptions

### 📸 Media Sharing

- **Image sharing** with preview
- **Video sharing** with playback
- **Audio messages** with voice recording
- **Document sharing** (PDF, DOC, TXT, etc.)
- **File upload** with drag-and-drop support

### 🔄 Status Updates (Stories)

- **24-hour status** that auto-expires
- **Text statuses** with custom background colors
- **Image/video statuses** support
- **Status views** tracking
- **Privacy controls** for status visibility

### 📞 Voice & Video Calls

- **Voice calling** with WebRTC
- **Video calling** with camera support
- **Call notifications** and ringtones
- **Accept/reject calls** functionality
- **End call** options

### 🔐 Authentication & Security

- **User registration** with validation
- **Secure login** with password hashing
- **Session management** with Flask-Login
- **Profile management** with avatar upload
- **About/bio** customization

### 🎨 Splinter Cell UI Theme

- **Dark green/black** color scheme
- **Glowing effects** and animations
- **Cyber-style** inputs and buttons
- **Scan-line animations** for that tactical feel
- **Pulse effects** on avatars and buttons
- **Orbitron & Rajdhani** fonts for that tech aesthetic

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory:**

```bash
cd c:\Users\matthew.ofomi\Desktop\FLASK_PROJECTS\flask_chat_app
```

2. **Activate the virtual environment:**

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

   Copy `.env.example` to `.env` and configure:

   ```bash
   copy .env.example .env
   ```

   **Important:** Get a FREE Groq API key for AI features:
   - Visit [https://console.groq.com/](https://console.groq.com/)
   - Sign up (free!)
   - Generate an API key
   - Add it to `.env`:
     ```
     GROQ_API_KEY=gsk_your_actual_key_here
     ```

5. **Initialize the AI bot (optional but recommended):**

```bash
python setup_ai_bot.py
```

6. **Run the application:**

```bash
python run.py
```

Or simply use the Windows launcher:

```bash
start.bat
```

7. **Access the application:**
   Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
flask_chat_app/
├── app/
│   ├── __init__.py          # App factory and configuration
│   ├── models.py            # Database models
│   ├── socket_events.py     # Socket.IO event handlers
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main app routes
│   │   ├── chat.py          # Chat functionality
│   │   ├── status.py        # Status/stories features
│   │   └── media.py         # Media upload/download
│   └── templates/
│       ├── base.html        # Base template with Splinter Cell theme
│       ├── auth/            # Login/register pages
│       ├── main/            # Main dashboard and profile
│       ├── chat/            # Chat interface
│       └── status/          # Status/stories pages
├── static/
│   └── uploads/             # User uploads (profiles, media, status)
├── venv/                    # Virtual environment
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
└── README.md               # This file
```

## 🎮 Usage Guide

### Creating an Account

1. Click "Register Access" on the login page
2. Fill in username, email, phone (optional), and password
3. Click "Register Operator"
4. Login with your credentials

### Starting a Chat

1. Click the "+" icon in the chat list
2. Select a user from the list
3. Start messaging!

### Creating a Group

1. Click the group icon in the header
2. Enter group name and description
3. Select members to add
4. Click "Create Group"

### Posting Status

1. Click the status icon (rotating circle)
2. Write your status text
3. Choose a background color
4. Click "Post Status" (visible for 24 hours)

### Making Calls

1. Open a chat with a user
2. Click the phone icon for voice call
3. Click the video icon for video call
4. Wait for the other user to accept

### Uploading Media

1. In a chat, click the paperclip icon
2. Select image, video, audio, or document
3. File will be uploaded and sent automatically

## 🎨 Color Scheme

The Splinter Cell theme uses these primary colors:

- **Splinter Green**: `#00ff41` - Primary accent color
- **Splinter Dark**: `#0a0e0f` - Main background
- **Splinter Darker**: `#060809` - Deeper backgrounds
- **Splinter Gray**: `#1a2426` - Cards and panels
- **Splinter Border**: `#1e3a30` - Border accents

## 🔧 Configuration

Edit `.env` file to customize:

```env
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///whatsapp.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB max file size
```

## 📦 Dependencies

- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **Flask-SocketIO** - Real-time communication
- **Pillow** - Image processing
- **Werkzeug** - Password hashing & security

## 🌟 Features Breakdown

### Real-Time Features (Socket.IO)

- ✅ Real-time message delivery
- ✅ Typing indicators
- ✅ Online/offline status
- ✅ Read receipts
- ✅ Call notifications
- ✅ WebRTC signaling

### Database Models

- **User** - User accounts and profiles
- **Message** - Text and media messages
- **Group** - Group chat metadata
- **Status** - 24-hour status updates
- **MessageReaction** - Emoji reactions
- **StatusView** - Status view tracking
- **TypingStatus** - Typing indicator states

### Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection (Flask default)
- File upload validation
- SQL injection prevention (SQLAlchemy ORM)

## 🚧 Development

### Running in Development Mode

```bash
python run.py
# App runs with debug=True on port 5000
```

### Database Reset

```bash
# Delete the database file
rm whatsapp.db

# Restart the app to recreate tables
python run.py
```

## 🎯 Future Enhancements

- [ ] End-to-end encryption
- [ ] Message forwarding
- [ ] Voice message playback speed
- [ ] GIF support
- [ ] Stickers
- [ ] Message search
- [ ] Archive chats
- [ ] Mute notifications
- [ ] Block users
- [ ] Report users
- [ ] Backup & restore
- [ ] Desktop notifications
- [ ] PWA support

## 📝 Notes

- The WebRTC implementation for calls is simplified and may require STUN/TURN servers for production
- File uploads are stored locally; consider cloud storage (S3, Azure Blob) for production
- Database uses SQLite for development; migrate to PostgreSQL/MySQL for production
- Status updates auto-expire after 24 hours (requires background job in production)

## 🤝 Contributing

This is a demonstration project. Feel free to fork and customize!

## 📄 License

This project is for educational purposes. WhatsApp is a registered trademark of Meta Platforms, Inc.

## 🎮 Controls & Shortcuts

- **Enter** - Send message
- **Ctrl+Enter** - New line in message
- **Esc** - Close modals
- **Tab** - Navigate between inputs

## 🔥 Performance Tips

- Clear browser cache if styles don't update
- Use Chrome/Firefox for best WebRTC support
- Ensure microphone/camera permissions for calls
- Keep browser updated for Socket.IO compatibility

## 💡 Troubleshooting

**Socket.IO not connecting?**

- Check if port 5000 is available
- Ensure no firewall blocking connections
- Try disabling browser extensions

**Files not uploading?**

- Check file size (max 16MB by default)
- Ensure uploads folder has write permissions
- Verify file type is allowed

**Database errors?**

- Delete `whatsapp.db` and restart app
- Check SQLAlchemy connection string
- Ensure no other process is using the database

---

**Built with ❤️ and lots of ☕ by a coding enthusiast**

_Remember: In the shadows, we thrive. In the chat, we connect._ 🟢
