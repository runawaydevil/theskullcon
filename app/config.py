import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = "your-secret-key-here"
    
    # Upload settings
    UPLOAD_FOLDER = "app/static/uploads"
    MAX_CONTENT_LENGTH = 300 * 1024 * 1024  # 300MB in bytes
    ALLOWED_EXTENSIONS = {
        'images': {'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'},
        'videos': {'mp4', 'avi', 'mov', 'mkv', 'gif'},
        'audio': {'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'}
    }
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 8012 