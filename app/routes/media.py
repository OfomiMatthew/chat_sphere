from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from PIL import Image

bp = Blueprint('media', __name__, url_prefix='/media')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mp3', 'wav', 'webm', 'ogg', 'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to make it unique
        timestamp = str(int(datetime.now().timestamp()))
        filename = f"{timestamp}_{filename}"
        
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'media')
        filepath = os.path.join(upload_folder, filename)
        
        file.save(filepath)
        
        # Determine file type
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in {'png', 'jpg', 'jpeg', 'gif'}:
            file_type = 'image'
        elif ext in {'mp4', 'avi', 'mov'}:
            file_type = 'video'
        elif ext in {'mp3', 'wav', 'webm', 'ogg'}:
            file_type = 'audio'
        else:
            file_type = 'document'
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': f'/static/uploads/media/{filename}',
            'type': file_type
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@bp.route('/upload-profile', methods=['POST'])
@login_required
def upload_profile():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Use user id in filename
        ext = filename.rsplit('.', 1)[1].lower()
        filename = f"profile_{current_user.id}.{ext}"
        
        upload_folder = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], 'profiles')
        filepath = os.path.join(upload_folder, filename)
        
        # Save and resize image
        file.save(filepath)
        
        # Resize image to 200x200
        with Image.open(filepath) as img:
            img = img.resize((200, 200), Image.LANCZOS)
            img.save(filepath)
        
        # Update user profile
        current_user.profile_pic = filename
        from app import db
        db.session.commit()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': f'/static/uploads/profiles/{filename}'
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

from datetime import datetime
