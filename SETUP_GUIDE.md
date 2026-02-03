# 🚀 Quick Setup Guide - ChatSphere with AI

Follow these steps to get ChatSphere running with all AI features enabled!

## Prerequisites

- Python 3.9 or higher
- Windows/Linux/Mac
- Internet connection (for AI features)

## Step-by-Step Setup

### 1️⃣ Navigate to Project Directory

```bash
cd c:\Users\matthew.ofomi\Desktop\FLASK_PROJECTS\flask_chat_app
```

### 2️⃣ Create/Activate Virtual Environment (if not already done)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- Flask 3.0.0
- Flask-SocketIO 5.3.6
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Groq 0.4.2 (AI features)
- And all other dependencies

### 4️⃣ Get Your FREE Groq API Key 🔑

**Why Groq?**

- FREE to use
- Ultra-fast AI inference (< 1 second responses)
- Access to powerful models (Llama 3.3 70B, Whisper)
- Generous rate limits

**How to get it:**

1. Go to **[https://console.groq.com/](https://console.groq.com/)**
2. Click "Sign Up" (you can use Google/GitHub)
3. Once logged in, click "API Keys" in left sidebar
4. Click "Create API Key"
5. Give it a name (e.g., "ChatSphere")
6. Copy the key (starts with `gsk_...`)

**⚠️ Important:** Save this key immediately! You won't be able to see it again.

### 5️⃣ Configure Environment Variables

**Option A: Use the example file**

```bash
copy .env.example .env
```

**Option B: Create .env manually**
Create a file named `.env` in the project root with:

```env
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=sqlite:///whatsapp.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
GROQ_API_KEY=gsk_paste_your_actual_key_here
```

**Important:** Replace `gsk_paste_your_actual_key_here` with your actual Groq API key!

### 6️⃣ Initialize the Database

The database will be created automatically on first run, but you can also run:

```bash
python setup_defaults.py
```

### 7️⃣ Create the AI Bot (Recommended)

```bash
python setup_ai_bot.py
```

This creates the `chatsphere_ai` user that you can chat with!

### 8️⃣ Start the Application

**Windows (Recommended):**

```bash
start.bat
```

**Or manually:**

```bash
python run.py
```

### 9️⃣ Access ChatSphere

Open your browser and go to:

```
http://localhost:5000
```

### 🔟 Create Your Account

1. Click "Register"
2. Fill in your details
3. Login
4. Start chatting!

---

## 🎉 Testing AI Features

### Try the AI Bot

1. Look for `chatsphere_ai` in the user list
2. Click to open a chat
3. Send any message like "Hello!" or "What can you do?"
4. The AI will respond automatically!

### Try Smart Replies

1. Open any chat
2. Click the "Smart Reply" button in the AI toolbar
3. Get 3 contextual suggestions
4. Click one to use it

### Try Message Enhancement

1. Type a message in the input box
2. Click the "Enhance" button
3. Select a tone (Professional, Casual, Friendly, etc.)
4. Click "Enhance" to see the improved version
5. Click "Use This" to put it in your message box

### Try Translation

1. Click the "Translate" button
2. Enter text or use your current message
3. Select target language
4. Click "Translate"

### Try Content Moderation

1. Click "Moderation: OFF" to enable it
2. Try sending a message
3. If flagged, you'll get a warning

### Try Conversation Summary

1. Have a conversation with someone (at least 5-10 messages)
2. Click the "Summarize" button
3. AI generates a summary of the entire conversation

### Try AI Search

1. Click the "AI Search" button
2. Enter a query like "messages about meeting"
3. AI finds relevant messages semantically

---

## 🐛 Troubleshooting

### Problem: AI features don't work

**Solution:**

1. Check that your GROQ_API_KEY is correctly set in `.env`
2. Verify the key at [console.groq.com](https://console.groq.com/)
3. Restart the application after adding the key
4. Check browser console (F12) for errors

### Problem: "Module not found" errors

**Solution:**

```bash
pip install -r requirements.txt
```

### Problem: Database errors

**Solution:**

```bash
# Delete the database and recreate it
del instance\whatsapp.db
python setup_defaults.py
python setup_ai_bot.py
```

### Problem: Port 5000 already in use

**Solution:**

- Stop other applications using port 5000
- Or edit `run.py` to use a different port

### Problem: WebRTC calls not working

**Solution:**

- Ensure you're using `http://localhost:5000` (not 127.0.0.1)
- Allow camera/microphone permissions in browser
- For production, use HTTPS

---

## 📖 Next Steps

1. **Read the full documentation:**
   - [AI Features Documentation](AI_FEATURES.md)
   - [Full README](README.md)

2. **Invite others:**
   - Share the URL with friends on the same network
   - They can register and start chatting!

3. **Customize:**
   - Change theme colors in templates
   - Add custom AI prompts in `app/ai_utils.py`
   - Extend with new features!

4. **Deploy (Future):**
   - Deploy to Heroku, AWS, or Azure
   - Set up HTTPS for WebRTC
   - Configure production database

---

## 💡 Pro Tips

1. **Smart Replies work better with context** - Have a few messages in the conversation first

2. **Message Enhancement** - Use "Concise" for long messages, "Professional" for work chats

3. **Content Moderation** - Enable for group chats to keep them safe

4. **AI Search** - Use natural language like "messages from last week about the project"

5. **Voice Transcription** - Send voice messages and transcribe them for accessibility

6. **Translation** - Great for international conversations

---

## 🎯 Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Start application
start.bat           # Windows
python run.py       # Any OS

# Setup AI bot
python setup_ai_bot.py

# Update database
python update_db.py

# Reset everything
del instance\whatsapp.db
python setup_defaults.py
python setup_ai_bot.py
```

---

## 🆘 Need Help?

1. Check the [AI_FEATURES.md](AI_FEATURES.md) documentation
2. Check the [README.md](README.md)
3. Look at the browser console (F12) for errors
4. Check Groq status at [status.groq.com](https://status.groq.com/)

---

**Happy Chatting with AI! 🚀🤖💬**
