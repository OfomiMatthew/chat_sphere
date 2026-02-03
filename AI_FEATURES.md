# 🤖 AI Features - ChatSphere

ChatSphere includes powerful AI features powered by Groq API, giving you access to cutting-edge language models for enhancing your chat experience.

## 🚀 Setup

1. **Get a Groq API Key** (FREE!)
   - Visit [https://console.groq.com/](https://console.groq.com/)
   - Sign up for a free account
   - Go to API Keys section
   - Generate a new API key

2. **Configure Your API Key**
   - Copy the `.env.example` file to `.env`
   - Replace `your-groq-api-key-here` with your actual Groq API key:
     ```
     GROQ_API_KEY=gsk_your_actual_key_here
     ```

3. **Restart the Application**
   - Stop the current server (Ctrl+C)
   - Run `start.bat` again

## ✨ AI Features

### 1. 🤖 AI Chat Assistant Bot

**How to use:**

- A special AI bot user `chatsphere_ai` is automatically created
- Look for "ChatSphere AI" in your contacts
- Start chatting! The AI can help with:
  - Answering questions
  - Providing recommendations
  - Explaining concepts
  - Creative writing
  - Problem solving
  - General conversation

**Endpoint:** `/ai/chat`

---

### 2. ✨ Smart Reply Suggestions

**How to use:**

- Click the "Smart Reply" button in the AI toolbar
- AI generates 3 contextual reply suggestions based on the conversation
- Click any suggestion to use it as your message

**Features:**

- Context-aware suggestions
- Natural, conversational responses
- Saves typing time

**Endpoint:** `/ai/smart-replies`

---

### 3. 🌐 Message Translation

**How to use:**

- Click the "Translate" button in the AI toolbar
- Enter text to translate (or it auto-fills from your message input)
- Select target language from dropdown
- Click "Translate" to see the result

**Supported Languages:**

- Spanish, French, German, Italian, Portuguese
- Chinese, Japanese, Korean
- Arabic, Russian
- And more!

**Endpoint:** `/ai/translate`

---

### 4. 🎨 Message Enhancement

**How to use:**

- Click the "Enhance" button in the AI toolbar
- Enter your message
- Choose a tone:
  - **Professional** - Polish for business communication
  - **Casual** - Relax for friendly chats
  - **Friendly** - Warm and approachable
  - **Formal** - Respectful and official
  - **Concise** - Shorter and to the point
- Click "Enhance" to see improved version
- Click "Use This" to put it in your message input

**Endpoint:** `/ai/enhance`

---

### 5. 🎤 Voice Message Transcription

**How to use:**

- Voice messages can be transcribed to text
- Uses Groq's Whisper model for accurate speech-to-text
- Helps with accessibility and searching voice messages

**Features:**

- Automatic transcription of audio
- Multi-language support
- High accuracy

**Endpoint:** `/ai/transcribe`

---

### 6. 🛡️ Content Moderation

**How to use:**

- Click the "Moderation: OFF" button to enable (turns green when ON)
- When enabled, AI checks messages before sending for:
  - Hate speech or discrimination
  - Explicit content
  - Violence or threats
  - Spam or scams
  - Personal attacks
- If content is flagged, you get a warning with option to send anyway

**Endpoint:** `/ai/moderate`

---

### 7. 😊 Sentiment Analysis

**How to use:**

- Analyzes the emotional tone of messages
- Returns sentiment (positive/negative/neutral)
- Provides confidence score
- Suggests appropriate emoji

**Use cases:**

- Understanding conversation tone
- Monitoring customer satisfaction
- Detecting conflicts early

**Endpoint:** `/ai/sentiment`

---

### 8. 📝 Conversation Summarization

**How to use:**

- Click the "Summarize" button in the AI toolbar
- AI generates a summary of the entire chat history
- Includes key points and action items
- Saves time reviewing long conversations

**Perfect for:**

- Catching up on missed messages
- Review meeting discussions
- Extract important information

**Endpoint:** `/ai/summarize`

---

### 9. 🔍 AI-Powered Smart Search

**How to use:**

- Click the "AI Search" button in the AI toolbar
- Enter a natural language query (e.g., "messages about the meeting")
- AI semantically searches through all messages
- Returns relevant messages ranked by relevance

**Features:**

- Understands context and intent
- Better than keyword search
- Finds messages even with different wording

**Endpoint:** `/ai/search`

---

### 10. ⌨️ Autocomplete (Built-in)

**How to use:**

- Start typing in the message input
- AI can suggest completions (feature ready, can be enabled in future)
- Context-aware based on conversation history

**Endpoint:** `/ai/autocomplete`

---

## 🔧 Technical Details

### Models Used

- **Chat/Text:** Llama 3.3 70B (fast, powerful, versatile)
- **Voice Transcription:** Whisper Large V3 (state-of-the-art speech recognition)

### API Limits

- Groq offers generous free tier
- Extremely fast inference (often < 1 second)
- No rate limiting for most use cases

### Performance

- All AI features are asynchronous
- Fast response times (typically < 2 seconds)
- Graceful error handling
- No blocking of chat functionality

## 🎯 Best Practices

1. **API Key Security**
   - Never commit `.env` file to git
   - Keep your API key private
   - Regenerate if exposed

2. **Content Moderation**
   - Enable for public/group chats
   - Customize rules in `ai_utils.py`
   - Review flagged content appropriately

3. **Smart Replies**
   - Best with recent conversation context
   - Works in both direct and group chats
   - Refresh suggestions if conversation changes

4. **Translation**
   - Best for complete sentences
   - May need adjustment for slang/idioms
   - Specify target language clearly

## 🐛 Troubleshooting

**AI features not working?**

1. Check that GROQ_API_KEY is set in `.env`
2. Verify API key is valid at [console.groq.com](https://console.groq.com/)
3. Check browser console for errors (F12)
4. Ensure stable internet connection

**Slow responses?**

- Groq is usually very fast (< 1s)
- Check your internet connection
- Try again if timeout occurs

**Translation issues?**

- Be specific about target language
- Use complete sentences
- Check for special characters

## 💡 Future Enhancements

Potential additions:

- Image captioning and analysis
- Meeting/call transcription and summaries
- Code explanation and generation
- Custom AI personalities
- Voice message AI responses
- Smart notifications with priority
- Automated task extraction

## 📚 Learn More

- [Groq Documentation](https://console.groq.com/docs)
- [Llama 3.3 Model Card](https://huggingface.co/meta-llama/Llama-3.3-70B)
- [Whisper Model](https://github.com/openai/whisper)

---

**Enjoy your AI-powered ChatSphere experience! 🚀🤖**
