from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for group members
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

# Association table for blocked users
blocked_users = db.Table('blocked_users',
    db.Column('blocker_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('blocked_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('blocked_at', db.DateTime, default=datetime.utcnow)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True)
    about = db.Column(db.String(200), default="Hey there! I am using ChatSphere")
    profile_pic = db.Column(db.String(255), default='default.png')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    statuses = db.relationship('Status', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    groups_owned = db.relationship('Group', backref='owner', lazy='dynamic')
    groups = db.relationship('Group', secondary=group_members, backref=db.backref('members', lazy='dynamic'))
    
    # Blocked users
    blocking = db.relationship('User', 
                              secondary=blocked_users,
                              primaryjoin=(blocked_users.c.blocker_id == id),
                              secondaryjoin=(blocked_users.c.blocked_id == id),
                              backref=db.backref('blocked_by', lazy='dynamic'),
                              lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_conversations(self):
        """Get all conversations (direct and group) for this user"""
        from sqlalchemy import or_, and_
        
        # Direct messages
        direct_messages = Message.query.filter(
            or_(
                Message.sender_id == self.id,
                Message.recipient_id == self.id
            ),
            Message.group_id == None
        ).order_by(Message.timestamp.desc()).all()
        
        # Get unique conversation partners
        conversation_partners = set()
        for msg in direct_messages:
            if msg.sender_id == self.id:
                conversation_partners.add(msg.recipient_id)
            else:
                conversation_partners.add(msg.sender_id)
        
        conversations = []
        for partner_id in conversation_partners:
            partner = User.query.get(partner_id)
            last_msg = Message.query.filter(
                or_(
                    and_(Message.sender_id == self.id, Message.recipient_id == partner_id),
                    and_(Message.sender_id == partner_id, Message.recipient_id == self.id)
                ),
                Message.group_id == None
            ).order_by(Message.timestamp.desc()).first()
            
            if last_msg:
                conversations.append({
                    'type': 'direct',
                    'user': partner,
                    'last_message': last_msg,
                    'unread_count': Message.query.filter_by(
                        sender_id=partner_id,
                        recipient_id=self.id,
                        is_read=False
                    ).count()
                })
        
        # Group messages
        for group in self.groups:
            last_msg = Message.query.filter_by(group_id=group.id).order_by(Message.timestamp.desc()).first()
            conversations.append({
                'type': 'group',
                'group': group,
                'last_message': last_msg if last_msg else type('obj', (object,), {
                    'content': 'No messages yet',
                    'timestamp': group.created_at,
                    'sender_id': None,
                    'message_type': 'text'
                })(),
                'unread_count': Message.query.filter(
                    Message.group_id == group.id,
                    Message.sender_id != self.id,
                    Message.is_read == False
                ).count() if last_msg else 0
            })
        
        # Sort by last message time
        conversations.sort(key=lambda x: x['last_message'].timestamp, reverse=True)
        return conversations

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    content = db.Column(db.Text)
    message_type = db.Column(db.String(20), default='text')  # text, image, video, audio, document, voice_call, video_call
    media_url = db.Column(db.String(255))
    call_duration = db.Column(db.Integer)  # Duration in seconds for call messages
    call_status = db.Column(db.String(20))  # missed, answered, declined for call messages
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, default=False)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)
    reply_to_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Relationships
    replies = db.relationship('Message', backref=db.backref('reply_to', remote_side=[id]), lazy='dynamic')
    reactions = db.relationship('MessageReaction', backref='message', lazy='dynamic', cascade='all, delete-orphan')

class MessageReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    emoji = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='reactions')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    group_pic = db.Column(db.String(255), default='default_group.png')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='group', lazy='dynamic', cascade='all, delete-orphan')

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    media_type = db.Column(db.String(20), default='text')  # text, image, video
    media_url = db.Column(db.String(255))
    background_color = db.Column(db.String(20), default='#075E54')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    views = db.relationship('StatusView', backref='status', lazy='dynamic', cascade='all, delete-orphan')

class StatusView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='status_views')

class TypingStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chat_with_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    is_typing = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
