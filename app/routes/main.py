from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User
from datetime import datetime
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Update last seen
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
    
    conversations = current_user.get_conversations()
    users = User.query.filter(User.id != current_user.id).all()
    
    return render_template('main/index.html', conversations=conversations, users=users)

@bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')
