from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Status, StatusView
from datetime import datetime, timedelta

bp = Blueprint('status', __name__, url_prefix='/status')

@bp.route('/')
@login_required
def index():
    # Get all active statuses (not expired)
    now = datetime.utcnow()
    
    # Get current user's statuses
    my_statuses = Status.query.filter(
        Status.user_id == current_user.id,
        Status.expires_at > now
    ).order_by(Status.created_at.desc()).all()
    
    # Get other users' statuses
    other_statuses = Status.query.filter(
        Status.user_id != current_user.id,
        Status.expires_at > now
    ).order_by(Status.created_at.desc()).all()
    
    # Group by user
    status_users = {}
    for status in other_statuses:
        if status.user_id not in status_users:
            status_users[status.user_id] = {
                'user': status.author,
                'statuses': [],
                'unseen_count': 0
            }
        status_users[status.user_id]['statuses'].append(status)
        
        # Check if current user has seen this status
        view = StatusView.query.filter_by(
            status_id=status.id,
            user_id=current_user.id
        ).first()
        
        if not view:
            status_users[status.user_id]['unseen_count'] += 1
    
    return render_template('status/index.html', 
                         my_statuses=my_statuses, 
                         status_users=status_users.values())

@bp.route('/create', methods=['POST'])
@login_required
def create():
    from werkzeug.utils import secure_filename
    import os
    from flask import current_app
    
    content = request.form.get('content', '')
    media_type = request.form.get('media_type', 'text')
    background_color = request.form.get('background_color', '#075E54')
    media_url = None
    
    # Handle file upload
    if 'media_file' in request.files:
        file = request.files['media_file']
        if file and file.filename:
            # Determine media type from file
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                media_type = 'image'
            elif file_ext in ['mp4', 'mov', 'avi', 'webm']:
                media_type = 'video'
            elif file_ext in ['mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac']:
                media_type = 'audio'
            
            # Create unique filename
            unique_filename = f"status_{current_user.id}_{datetime.utcnow().timestamp()}_{filename}"
            
            # Save file
            upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'status')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            media_url = f"/static/uploads/status/{unique_filename}"
    
    # Create status that expires in 24 hours
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    status = Status(
        user_id=current_user.id,
        content=content,
        media_type=media_type,
        media_url=media_url,
        background_color=background_color,
        expires_at=expires_at
    )
    
    db.session.add(status)
    db.session.commit()
    
    return jsonify({'success': True, 'status_id': status.id})

@bp.route('/view/<int:status_id>', methods=['POST'])
@login_required
def view_status(status_id):
    status = Status.query.get_or_404(status_id)
    
    # Check if already viewed
    existing_view = StatusView.query.filter_by(
        status_id=status_id,
        user_id=current_user.id
    ).first()
    
    if not existing_view:
        view = StatusView(
            status_id=status_id,
            user_id=current_user.id
        )
        db.session.add(view)
        db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/delete/<int:status_id>', methods=['POST'])
@login_required
def delete(status_id):
    status = Status.query.get_or_404(status_id)
    
    if status.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    db.session.delete(status)
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_statuses(user_id):
    """Get all active statuses for a specific user"""
    now = datetime.utcnow()
    
    statuses = Status.query.filter(
        Status.user_id == user_id,
        Status.expires_at > now
    ).order_by(Status.created_at.asc()).all()
    
    status_data = []
    for status in statuses:
        # Check if current user has viewed this status
        view = StatusView.query.filter_by(
            status_id=status.id,
            user_id=current_user.id
        ).first()
        
        status_data.append({
            'id': status.id,
            'content': status.content,
            'media_type': status.media_type,
            'media_url': status.media_url,
            'background_color': status.background_color,
            'created_at': status.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'expires_at': status.expires_at.strftime('%Y-%m-%d %H:%M:%S'),
            'viewed': view is not None,
            'view_count': StatusView.query.filter_by(status_id=status.id).count()
        })
    
    # Get user info
    from app.models import User
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'profile_pic': user.profile_pic
        },
        'statuses': status_data
    })
