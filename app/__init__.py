from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO(cors_allowed_origins="*", manage_session=False)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///whatsapp.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
    app.config['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY', '')
    
    # Ensure upload folder exists
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'media'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'status'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app)
    
    # Import models
    from app import models
    
    # Register socket event handlers
    from app import socket_events
    
    # Register blueprints
    from app.routes import auth, main, chat, status, media, ai
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(status.bp)
    app.register_blueprint(media.bp)
    app.register_blueprint(ai.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
