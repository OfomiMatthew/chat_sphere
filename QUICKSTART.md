# 🚀 QUICK START GUIDE

## Application is Running! 🎉

Your WhatsApp Clone with Splinter Cell theme is now live at:
**http://localhost:5000**

---

## 📋 First Steps

### 1. Create Your Account

- Navigate to http://localhost:5000
- Click "Register Access"
- Fill in:
  - Username (e.g., "Agent47")
  - Email (e.g., "agent@splintercell.com")
  - Phone (optional)
  - Password
- Click "Register Operator"

### 2. Login

- Enter your username and password
- Click "Initiate Login"
- You'll be taken to the main dashboard

### 3. Create Another User (Testing)

- Open a new incognito/private browser window
- Go to http://localhost:5000
- Register a second user
- This allows you to test messaging between users

---

## 💬 Using the Chat Features

### Starting a Direct Chat

1. Click the **message icon** (+ with comment bubble) in the header
2. Select a user from the list
3. Type your message and press **Enter** or click send
4. You'll see:
   - ✓✓ Read receipts
   - Typing indicators when they type
   - Online/offline status

### Creating a Group

1. Click the **group icon** (people icon) in the header
2. Enter group name (e.g., "Strike Team Alpha")
3. Add description (optional)
4. Select members to add
5. Click "Create Group"
6. Start group messaging!

### Sending Media

1. In any chat, click the **paperclip icon**
2. Select file (images, videos, audio, documents)
3. File uploads and sends automatically
4. Supports: PNG, JPG, MP4, MP3, PDF, DOC, TXT

### Voice Messages

1. Click the **microphone icon**
2. Browser will ask for mic permission
3. Click OK in the alert to record
4. Recording sends automatically when you click OK again

### Message Features

- **Delete**: Click trash icon under your messages
- **React**: Hover and click emoji button (to be implemented)
- **Reply**: Click reply icon (to be implemented)

---

## 📸 Status Updates (Stories)

### Posting Status

1. Click the **rotating circle icon** in header OR
2. Go to Status section from sidebar
3. Click "Create Status"
4. Write your message
5. Choose background color (10 colors available)
6. Click "Post Status"
7. Status visible for 24 hours!

### Viewing Status

- Your status shows at top with green ring
- Friends' status shows below
- Green ring = unseen updates
- Gray ring = already viewed
- Click to view status

---

## 📞 Voice & Video Calls

### Making a Call

1. Open a direct chat
2. Click **phone icon** for voice call
3. Click **video icon** for video call
4. Browser will ask for camera/mic permissions
5. Wait for other user to accept

### Receiving a Call

- Alert pops up when someone calls
- Click OK to accept
- Click Cancel to reject
- Call interface shows with end call button

**Note**: WebRTC calls work best on:

- Chrome/Edge (best support)
- Firefox (good support)
- Local network or same device (best testing)

---

## 👤 Profile Management

### Updating Profile Picture

1. Click your avatar in top-left
2. Or navigate to Profile section
3. Click camera icon on your avatar
4. Select image file
5. Image automatically resizes to 200x200px
6. Profile pic updates across all chats!

### Updating About/Bio

1. Go to Profile section
2. Edit the "About" text field
3. Click checkmark to save
4. Shows in your profile and chat info

---

## 🎨 Theme Features

The Splinter Cell theme includes:

### Visual Effects

- **Glowing text** on important elements
- **Pulse animations** on avatars
- **Scan-line effects** on headers
- **Hover effects** that glow green
- **Cyber-style buttons** with slide animations
- **Message bubbles** with gradient backgrounds

### Colors

- Sent messages: Dark green gradient
- Received messages: Dark gray gradient
- Accents: Bright green (#00ff41)
- Background: Deep black/dark green

---

## ⌨️ Keyboard Shortcuts

- **Enter** - Send message
- **Esc** - Close any modal
- **Tab** - Navigate between fields
- Type to see typing indicator on other user's screen

---

## 🔍 Testing Scenarios

### Test Real-Time Messaging

1. Open app in 2 different browsers/windows
2. Login as different users
3. Send messages - see instant delivery
4. Watch typing indicators appear
5. Check read receipts

### Test Group Functionality

1. Create group with 3+ users
2. All members see messages instantly
3. Member names show on messages
4. Test with multiple browser windows

### Test File Uploads

1. Upload different file types
2. Check previews for images
3. Play videos inline
4. Download documents

---

## 🐛 Troubleshooting

### Can't Connect?

- Check terminal shows "Running on http://127.0.0.1:5000"
- Try http://localhost:5000 or http://127.0.0.1:5000
- Disable VPN if active
- Check firewall isn't blocking port 5000

### Files Not Uploading?

- Max file size: 16MB
- Allowed types: images, videos, audio, documents
- Check uploads folder has write permissions
- Try smaller file

### Socket.IO Issues?

- Refresh browser page
- Clear browser cache (Ctrl+Shift+Del)
- Check browser console for errors (F12)
- Ensure no extensions blocking WebSocket

### Database Errors?

```bash
# Reset database
del whatsapp.db
# Restart app
python run.py
```

### Calls Not Working?

- Allow camera/microphone permissions
- Use Chrome or Firefox
- Test on same device first
- Check browser supports WebRTC

---

## 🎯 Advanced Features

### Database Location

- SQLite file: `whatsapp.db` (created automatically)
- View with: DB Browser for SQLite

### Upload Folders

- Profiles: `static/uploads/profiles/`
- Media: `static/uploads/media/`
- Status: `static/uploads/status/`

### Environment Variables

Edit `.env` file:

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///whatsapp.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Running on Different Port

Edit `run.py`:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=8080)
```

---

## 📊 Statistics

Your profile shows:

- **Total messages** sent
- **Groups** you're in
- **Status updates** posted

---

## 🎓 Learning Resources

### Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy + SQLite
- **Real-time**: Flask-SocketIO + Socket.IO
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Authentication**: Flask-Login
- **Media**: Pillow (image processing)

### Code Structure

```
app/
  ├── models.py         → Database schemas
  ├── routes/          → URL endpoints
  │   ├── auth.py      → Login/register
  │   ├── chat.py      → Messaging
  │   ├── status.py    → Stories
  │   └── media.py     → File uploads
  ├── socket_events.py → Real-time events
  └── templates/       → HTML pages
```

---

## 🌟 Feature Highlights

✅ Real-time messaging with Socket.IO
✅ Read receipts (double check marks)
✅ Typing indicators
✅ Online/offline status
✅ Last seen timestamps
✅ Group chats with unlimited members
✅ Media sharing (images, videos, audio, docs)
✅ 24-hour status updates
✅ Voice recording
✅ Video/voice calls (WebRTC)
✅ Profile pictures
✅ Custom avatars (auto-generated)
✅ Message deletion
✅ Splinter Cell theme (dark green/black)
✅ Glowing animations
✅ Cyber-style UI
✅ Mobile-responsive design

---

## 🚀 Next Steps

1. **Test all features** - messaging, groups, status, calls
2. **Customize theme** - edit colors in base.html
3. **Add features** - check README for enhancement ideas
4. **Deploy** - consider Heroku, PythonAnywhere, or AWS

---

## 📞 Support

Having issues? Check:

1. README.md - Full documentation
2. Terminal output - Error messages
3. Browser console (F12) - JavaScript errors
4. requirements.txt - Dependency versions

---

## 🎮 Have Fun!

You now have a fully-functional WhatsApp clone with:

- Military-grade aesthetics (Splinter Cell theme)
- Real-time communication
- All core WhatsApp features
- Sleek, responsive design

**Enjoy your secure communications system!** 🟢

---

_Built with Flask • Styled with TailwindCSS • Powered by Socket.IO_
