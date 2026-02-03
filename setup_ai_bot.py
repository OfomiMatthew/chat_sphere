"""
Initialize AI Bot User
Run this script once to create the ChatSphere AI bot user
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if AI bot already exists
    ai_bot = User.query.filter_by(username='chatsphere_ai').first()
    
    if ai_bot:
        print("✅ ChatSphere AI bot already exists!")
        print(f"   Username: {ai_bot.username}")
        print(f"   ID: {ai_bot.id}")
    else:
        # Create AI bot user
        ai_bot = User(
            username='chatsphere_ai',
            email='ai@chatsphere.app',
            phone='0000000000',
            about='I am ChatSphere AI Assistant 🤖 Ask me anything!',
            profile_pic='ai_bot.png'
        )
        ai_bot.set_password('impossible_password_that_cannot_be_guessed_12345!@#$%')
        
        db.session.add(ai_bot)
        db.session.commit()
        
        print("✅ ChatSphere AI bot created successfully!")
        print(f"   Username: {ai_bot.username}")
        print(f"   ID: {ai_bot.id}")
        print("\nThe AI bot will automatically respond to messages sent to it.")
        print("Users can start a chat with 'chatsphere_ai' to talk to the AI assistant!")
