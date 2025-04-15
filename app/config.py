import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Upload settings
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app', 'static')
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'app', 'templates')
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # 300MB
    CLEANUP_INTERVAL = 3600  # 1 hour in seconds
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 8012
    DEBUG = True
    
    # Allowed file extensions
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.gif'}
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Audio extensions
    ALLOWED_AUDIO_EXTENSIONS = {
        'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'
    }
    
    # Allowed extensions
    ALLOWED_EXTENSIONS = {
        'images': ALLOWED_IMAGE_EXTENSIONS,
        'videos': ALLOWED_VIDEO_EXTENSIONS,
        'audio': ALLOWED_AUDIO_EXTENSIONS
    } 