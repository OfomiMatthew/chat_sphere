from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from app.models import Message
from datetime import datetime
import traceback

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        current_user.is_online = True
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        emit('user_online', {'user_id': current_user.id}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        current_user.is_online = False
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        emit('user_offline', {'user_id': current_user.id}, broadcast=True)

@socketio.on('join_chat')
def handle_join_chat(data):
    room = data.get('room')
    join_room(room)
    emit('joined_chat', {'room': room}, room=room)

@socketio.on('leave_chat')
def handle_leave_chat(data):
    room = data.get('room')
    leave_room(room)

@socketio.on('send_message')
def handle_send_message(data):
    try:
        print(f"Received send_message event from user {current_user.id}: {data}")
        
        recipient_id = data.get('recipient_id')
        group_id = data.get('group_id')
        content = data.get('content')
        message_type = data.get('message_type', 'text')
        media_url = data.get('media_url')
        
        if not content and not media_url:
            print("Error: No content or media_url provided")
            emit('error', {'message': 'No content provided'})
            return
        
        # Create message
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            group_id=group_id,
            content=content,
            message_type=message_type,
            media_url=media_url,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(message)
        db.session.commit()
        
        print(f"Message saved to database with ID: {message.id}")
        
        # Prepare message data
        message_data = {
            'id': message.id,
            'sender_id': current_user.id,
            'sender_name': current_user.username,
            'sender_pic': current_user.profile_pic,
            'recipient_id': recipient_id,
            'group_id': group_id,
            'content': content,
            'message_type': message_type,
            'media_url': media_url,
            'timestamp': message.timestamp.isoformat(),
            'is_read': False
        }
        
        # Emit to appropriate room
        if group_id:
            room = f'group_{group_id}'
            print(f"Emitting to group room: {room}")
            emit('new_message', message_data, room=room, include_self=True)
        else:
            # Send to recipient
            room = f'user_{recipient_id}'
            print(f"Emitting to recipient room: {room}")
            emit('new_message', message_data, room=room)
            
            # Send to sender (for multi-device support)
            room_sender = f'user_{current_user.id}'
            print(f"Emitting to sender room: {room_sender}")
            emit('new_message', message_data, room=room_sender)
        
        print("Message sent successfully!")
        
    except Exception as e:
        print(f"Error in handle_send_message: {str(e)}")
        print(traceback.format_exc())
        emit('error', {'message': str(e)})

@socketio.on('typing')
def handle_typing(data):
    recipient_id = data.get('recipient_id')
    group_id = data.get('group_id')
    is_typing = data.get('is_typing', False)
    
    typing_data = {
        'user_id': current_user.id,
        'username': current_user.username,
        'is_typing': is_typing
    }
    
    if group_id:
        room = f'group_{group_id}'
        emit('user_typing', typing_data, room=room, include_self=False)
    elif recipient_id:
        room = f'user_{recipient_id}'
        emit('user_typing', typing_data, room=room)

@socketio.on('message_read')
def handle_message_read(data):
    message_ids = data.get('message_ids', [])
    
    for msg_id in message_ids:
        message = Message.query.get(msg_id)
        if message and message.recipient_id == current_user.id:
            message.is_read = True
            message.read_at = datetime.utcnow()
    
    db.session.commit()
    
    # Notify sender
    if message_ids:
        first_message = Message.query.get(message_ids[0])
        if first_message:
            room = f'user_{first_message.sender_id}'
            emit('messages_read', {'message_ids': message_ids}, room=room)

@socketio.on('start_call')
def handle_start_call(data):
    recipient_id = data.get('recipient_id')
    call_type = data.get('call_type', 'voice')  # voice or video
    
    call_data = {
        'caller_id': current_user.id,
        'caller_name': current_user.username,
        'caller_pic': current_user.profile_pic,
        'call_type': call_type,
        'room_id': data.get('room_id')
    }
    
    room = f'user_{recipient_id}'
    emit('incoming_call', call_data, room=room)

@socketio.on('call_initiate')
def handle_call_initiate(data):
    """Handle WebRTC call initiation with offer"""
    recipient_id = data.get('recipient_id')
    call_type = data.get('call_type', 'voice')
    room_id = data.get('room_id')
    offer = data.get('offer')
    
    call_data = {
        'caller_id': current_user.id,
        'caller_name': current_user.username,
        'caller_pic': current_user.profile_pic,
        'call_type': call_type,
        'room_id': room_id,
        'offer': offer
    }
    
    room = f'user_{recipient_id}'
    emit('incoming_call', call_data, room=room)

@socketio.on('call_answer')
def handle_call_answer(data):
    """Handle WebRTC call answer"""
    caller_id = data.get('caller_id')
    room_id = data.get('room_id')
    answer = data.get('answer')
    
    room = f'user_{caller_id}'
    emit('call_answered', {
        'room_id': room_id,
        'answer': answer
    }, room=room)

@socketio.on('call_reject')
def handle_call_reject(data):
    """Handle call rejection"""
    caller_id = data.get('caller_id')
    
    room = f'user_{caller_id}'
    emit('call_rejected', {}, room=room)

@socketio.on('call_end')
def handle_call_end(data):
    """Handle call termination"""
    recipient_id = data.get('recipient_id')
    room_id = data.get('room_id')
    
    if recipient_id:
        room = f'user_{recipient_id}'
        emit('call_ended', {'room_id': room_id}, room=room)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    """Handle ICE candidate exchange"""
    recipient_id = data.get('recipient_id')
    candidate = data.get('candidate')
    room_id = data.get('room_id')
    
    if recipient_id:
        room = f'user_{recipient_id}'
        emit('ice_candidate_received', {
            'candidate': candidate,
            'room_id': room_id
        }, room=room)

@socketio.on('accept_call')
def handle_accept_call(data):
    # Keep for backward compatibility
    caller_id = data.get('caller_id')
    room_id = data.get('room_id')
    
    room = f'user_{caller_id}'
    emit('call_accepted', {'room_id': room_id}, room=room)

@socketio.on('reject_call')
def handle_reject_call(data):
    # Keep for backward compatibility
    caller_id = data.get('caller_id')
    
    room = f'user_{caller_id}'
    emit('call_rejected', {}, room=room)

@socketio.on('end_call')
def handle_end_call(data):
    # Keep for backward compatibility
    recipient_id = data.get('recipient_id')
    
    room = f'user_{recipient_id}'
    emit('call_ended', {}, room=room)

@socketio.on('webrtc_offer')
def handle_webrtc_offer(data):
    # Kept for backward compatibility if needed
    recipient_id = data.get('recipient_id')
    offer = data.get('offer')
    
    room = f'user_{recipient_id}'
    emit('webrtc_offer', {'offer': offer, 'sender_id': current_user.id}, room=room)

@socketio.on('webrtc_answer')
def handle_webrtc_answer(data):
    # Kept for backward compatibility if needed
    recipient_id = data.get('recipient_id')
    answer = data.get('answer')
    
    room = f'user_{recipient_id}'
    emit('webrtc_answer', {'answer': answer}, room=room)

@socketio.on('webrtc_ice_candidate')
def handle_webrtc_ice_candidate_legacy(data):
    # Kept for backward compatibility if needed
    recipient_id = data.get('recipient_id')
    candidate = data.get('candidate')
    
    room = f'user_{recipient_id}'
    emit('webrtc_ice_candidate', {'candidate': candidate}, room=room)

@socketio.on('log_call')
def handle_log_call(data):
    """Log a call in the chat history"""
    try:
        recipient_id = data.get('recipient_id')
        call_type = data.get('call_type')  # 'voice_call' or 'video_call'
        call_duration = data.get('duration', 0)  # Duration in seconds
        call_status = data.get('status', 'answered')  # 'answered', 'missed', 'declined'
        
        # Create call log message
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            message_type=call_type,
            call_duration=call_duration,
            call_status=call_status,
            content=f"{call_type.replace('_', ' ').title()}",
            timestamp=datetime.utcnow()
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Prepare message data
        message_data = {
            'id': message.id,
            'sender_id': current_user.id,
            'sender_name': current_user.username,
            'recipient_id': recipient_id,
            'content': message.content,
            'message_type': call_type,
            'call_duration': call_duration,
            'call_status': call_status,
            'timestamp': message.timestamp.isoformat()
        }
        
        # Emit to both users
        room_recipient = f'user_{recipient_id}'
        emit('new_message', message_data, room=room_recipient)
        
        room_sender = f'user_{current_user.id}'
        emit('new_message', message_data, room=room_sender)
        
        emit('call_logged', {'message_id': message.id})
        
    except Exception as e:
        print(f"Error logging call: {str(e)}")
        print(traceback.format_exc())
