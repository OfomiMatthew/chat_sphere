from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Message, User, Group, MessageReaction
from datetime import datetime
from sqlalchemy import or_, and_

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/user/<int:user_id>')
@login_required
def user_chat(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get messages between current user and selected user
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        ),
        Message.group_id == None,
        Message.is_deleted == False
    ).order_by(Message.timestamp.asc()).all()
    
    # Mark messages as read
    unread_messages = Message.query.filter_by(
        sender_id=user_id,
        recipient_id=current_user.id,
        is_read=False
    ).all()
    
    for msg in unread_messages:
        msg.is_read = True
        msg.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return render_template('chat/chat.html', chat_user=user, messages=messages, chat_type='user')

@bp.route('/group/<int:group_id>')
@login_required
def group_chat(group_id):
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member
    if current_user not in group.members.all():
        return "Not authorized", 403
    
    messages = Message.query.filter_by(
        group_id=group_id,
        is_deleted=False
    ).order_by(Message.timestamp.asc()).all()
    
    return render_template('chat/chat.html', group=group, messages=messages, chat_type='group')

@bp.route('/messages/user/<int:user_id>')
@login_required
def get_user_messages(user_id):
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        ),
        Message.group_id == None,
        Message.is_deleted == False
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify([{
        'id': msg.id,
        'sender_id': msg.sender_id,
        'content': msg.content,
        'message_type': msg.message_type,
        'media_url': msg.media_url,
        'timestamp': msg.timestamp.isoformat(),
        'is_read': msg.is_read,
        'sender_name': msg.sender.username,
        'sender_pic': msg.sender.profile_pic
    } for msg in messages])

@bp.route('/messages/group/<int:group_id>')
@login_required
def get_group_messages(group_id):
    group = Group.query.get_or_404(group_id)
    
    if current_user not in group.members.all():
        return jsonify({'error': 'Not authorized'}), 403
    
    messages = Message.query.filter_by(
        group_id=group_id,
        is_deleted=False
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify([{
        'id': msg.id,
        'sender_id': msg.sender_id,
        'content': msg.content,
        'message_type': msg.message_type,
        'media_url': msg.media_url,
        'timestamp': msg.timestamp.isoformat(),
        'sender_name': msg.sender.username,
        'sender_pic': msg.sender.profile_pic
    } for msg in messages])

@bp.route('/create-group', methods=['POST'])
@login_required
def create_group():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    member_ids = data.get('members', [])
    
    group = Group(
        name=name,
        description=description,
        owner_id=current_user.id
    )
    
    # Add owner as member
    group.members.append(current_user)
    
    # Add other members
    for member_id in member_ids:
        user = User.query.get(member_id)
        if user:
            group.members.append(user)
    
    db.session.add(group)
    db.session.commit()
    
    return jsonify({'success': True, 'group_id': group.id})

@bp.route('/delete-message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    if message.sender_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    message.is_deleted = True
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/group/<int:group_id>/available-users')
@login_required
def get_available_users(group_id):
    group = Group.query.get_or_404(group_id)
    
    # Check if user is member
    if current_user not in group.members.all():
        return jsonify({'error': 'Not authorized'}), 403
    
    # Get all users except current members
    current_member_ids = [member.id for member in group.members.all()]
    available_users = User.query.filter(~User.id.in_(current_member_ids)).all()
    
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'about': user.about,
        'profile_pic': user.profile_pic
    } for user in available_users])

@bp.route('/group/<int:group_id>/add-member', methods=['POST'])
@login_required
def add_member_to_group(group_id):
    group = Group.query.get_or_404(group_id)
    
    # Check if user is group owner or member
    if current_user not in group.members.all():
        return jsonify({'error': 'Not authorized'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    
    user = User.query.get_or_404(user_id)
    
    # Check if user is already a member
    if user in group.members.all():
        return jsonify({'error': 'User is already a member'}), 400
    
    group.members.append(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{user.username} added to group'})

@bp.route('/react/<int:message_id>', methods=['POST'])
@login_required
def react_to_message(message_id):
    data = request.get_json()
    emoji = data.get('emoji')
    
    message = Message.query.get_or_404(message_id)
    
    # Check if user already reacted
    existing_reaction = MessageReaction.query.filter_by(
        message_id=message_id,
        user_id=current_user.id
    ).first()
    
    if existing_reaction:
        existing_reaction.emoji = emoji
    else:
        reaction = MessageReaction(
            message_id=message_id,
            user_id=current_user.id,
            emoji=emoji
        )
        db.session.add(reaction)
    
    db.session.commit()
    
    return jsonify({'success': True})
