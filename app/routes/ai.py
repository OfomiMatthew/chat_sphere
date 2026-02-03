"""
AI Routes for ChatSphere
Handles all AI feature endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Message, User, Group
from app.ai_utils import (
    generate_smart_replies, translate_message, enhance_message,
    transcribe_audio, moderate_content, analyze_sentiment,
    summarize_conversation, smart_search, get_ai_response,
    autocomplete_text
)
from datetime import datetime
import os

bp = Blueprint('ai', __name__, url_prefix='/ai')

# AI Bot User ID (will be created in setup)
AI_BOT_ID = None

def get_ai_bot():
    """Get or create AI bot user"""
    global AI_BOT_ID
    if AI_BOT_ID:
        return User.query.get(AI_BOT_ID)
    
    ai_bot = User.query.filter_by(username='chatsphere_ai').first()
    if not ai_bot:
        ai_bot = User(
            username='chatsphere_ai',
            email='ai@chatsphere.app',
            phone='0000000000',
            about='I am ChatSphere AI Assistant 🤖 Ask me anything!',
            profile_pic='ai_bot.png'
        )
        ai_bot.set_password('impossible_password_12345')
        db.session.add(ai_bot)
        db.session.commit()
    
    AI_BOT_ID = ai_bot.id
    return ai_bot

@bp.route('/chat', methods=['POST'])
@login_required
def ai_chat():
    """Send message to AI bot and get response"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    
    ai_bot = get_ai_bot()
    
    # Get conversation history
    history = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.recipient_id == ai_bot.id),
            db.and_(Message.sender_id == ai_bot.id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.timestamp.desc()).limit(20).all()
    
    history_data = [{
        'content': msg.content,
        'is_ai': msg.sender_id == ai_bot.id
    } for msg in reversed(history)]
    
    # Get AI response
    ai_response = get_ai_response(user_message, history_data)
    
    # Save AI response as message
    ai_message = Message(
        sender_id=ai_bot.id,
        recipient_id=current_user.id,
        content=ai_response,
        message_type='text',
        timestamp=datetime.utcnow()
    )
    db.session.add(ai_message)
    db.session.commit()
    
    return jsonify({
        'response': ai_response,
        'message_id': ai_message.id,
        'timestamp': ai_message.timestamp.isoformat()
    })

@bp.route('/smart-replies', methods=['POST'])
@login_required
def smart_replies():
    """Generate smart reply suggestions"""
    data = request.get_json()
    chat_type = data.get('chat_type', 'user')
    chat_id = data.get('chat_id')
    
    if not chat_id:
        return jsonify({'error': 'chat_id required'}), 400
    
    # Get recent messages
    if chat_type == 'user':
        messages = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.recipient_id == chat_id),
                db.and_(Message.sender_id == chat_id, Message.recipient_id == current_user.id)
            )
        ).order_by(Message.timestamp.desc()).limit(10).all()
    else:
        messages = Message.query.filter_by(group_id=chat_id).order_by(Message.timestamp.desc()).limit(10).all()
    
    message_history = [{
        'sender': User.query.get(msg.sender_id).username,
        'content': msg.content
    } for msg in reversed(messages) if msg.message_type == 'text']
    
    replies = generate_smart_replies(message_history)
    return jsonify({'replies': replies})

@bp.route('/translate', methods=['POST'])
@login_required
def translate():
    """Translate message"""
    data = request.get_json()
    text = data.get('text', '').strip()
    language = data.get('language', 'English')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    translated = translate_message(text, language)
    return jsonify({'translated': translated})

@bp.route('/enhance', methods=['POST'])
@login_required
def enhance():
    """Enhance message with specified tone"""
    data = request.get_json()
    text = data.get('text', '').strip()
    tone = data.get('tone', 'professional')
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    enhanced = enhance_message(text, tone)
    return jsonify({'enhanced': enhanced})

@bp.route('/transcribe', methods=['POST'])
@login_required
def transcribe():
    """Transcribe audio message"""
    data = request.get_json()
    message_id = data.get('message_id')
    
    if not message_id:
        return jsonify({'error': 'message_id required'}), 400
    
    message = Message.query.get(message_id)
    if not message or message.message_type != 'voice':
        return jsonify({'error': 'Invalid voice message'}), 400
    
    # Check if user has access to this message
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        if not message.group_id or current_user not in Group.query.get(message.group_id).members:
            return jsonify({'error': 'Access denied'}), 403
    
    audio_path = os.path.join(current_app.root_path, message.media_url)
    if not os.path.exists(audio_path):
        return jsonify({'error': 'Audio file not found'}), 404
    
    transcription = transcribe_audio(audio_path)
    return jsonify({'transcription': transcription})

@bp.route('/moderate', methods=['POST'])
@login_required
def moderate():
    """Check if message content is appropriate"""
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    result = moderate_content(text)
    return jsonify(result)

@bp.route('/sentiment', methods=['POST'])
@login_required
def sentiment():
    """Analyze message sentiment"""
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    result = analyze_sentiment(text)
    return jsonify(result)

@bp.route('/summarize', methods=['POST'])
@login_required
def summarize():
    """Summarize conversation"""
    data = request.get_json()
    chat_type = data.get('chat_type', 'user')
    chat_id = data.get('chat_id')
    max_length = data.get('max_length', 200)
    
    if not chat_id:
        return jsonify({'error': 'chat_id required'}), 400
    
    # Get all messages from conversation
    if chat_type == 'user':
        messages = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.recipient_id == chat_id),
                db.and_(Message.sender_id == chat_id, Message.recipient_id == current_user.id)
            )
        ).order_by(Message.timestamp.asc()).all()
    else:
        group = Group.query.get(chat_id)
        if not group or current_user not in group.members:
            return jsonify({'error': 'Access denied'}), 403
        messages = Message.query.filter_by(group_id=chat_id).order_by(Message.timestamp.asc()).all()
    
    if not messages:
        return jsonify({'summary': 'No messages to summarize'}), 200
    
    message_data = [{
        'sender': User.query.get(msg.sender_id).username,
        'content': msg.content
    } for msg in messages if msg.message_type == 'text']
    
    summary = summarize_conversation(message_data, max_length)
    return jsonify({'summary': summary})

@bp.route('/search', methods=['POST'])
@login_required
def search():
    """Semantic search through messages"""
    data = request.get_json()
    query = data.get('query', '').strip()
    chat_type = data.get('chat_type', 'user')
    chat_id = data.get('chat_id')
    
    if not query or not chat_id:
        return jsonify({'error': 'Query and chat_id required'}), 400
    
    # Get all messages from conversation
    if chat_type == 'user':
        messages = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.recipient_id == chat_id),
                db.and_(Message.sender_id == chat_id, Message.recipient_id == current_user.id)
            )
        ).order_by(Message.timestamp.asc()).all()
    else:
        messages = Message.query.filter_by(group_id=chat_id).order_by(Message.timestamp.asc()).all()
    
    message_data = [{
        'id': msg.id,
        'sender': User.query.get(msg.sender_id).username,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat()
    } for msg in messages if msg.message_type == 'text']
    
    results = smart_search(query, message_data)
    return jsonify({'results': results})

@bp.route('/autocomplete', methods=['POST'])
@login_required
def autocomplete():
    """Get text completion suggestions"""
    data = request.get_json()
    partial_text = data.get('text', '').strip()
    chat_type = data.get('chat_type', 'user')
    chat_id = data.get('chat_id')
    
    if not partial_text or len(partial_text) < 3:
        return jsonify({'completions': []})
    
    # Get recent context
    context = ""
    if chat_id:
        if chat_type == 'user':
            messages = Message.query.filter(
                db.or_(
                    db.and_(Message.sender_id == current_user.id, Message.recipient_id == chat_id),
                    db.and_(Message.sender_id == chat_id, Message.recipient_id == current_user.id)
                )
            ).order_by(Message.timestamp.desc()).limit(3).all()
        else:
            messages = Message.query.filter_by(group_id=chat_id).order_by(Message.timestamp.desc()).limit(3).all()
        
        context = " ".join([msg.content for msg in reversed(messages) if msg.message_type == 'text'])
    
    completions = autocomplete_text(partial_text, context)
    return jsonify({'completions': completions})
