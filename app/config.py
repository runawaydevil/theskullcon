import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
    
    # Configurações de upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configurações de conversão
    ALLOWED_EXTENSIONS = {
        'image': ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'],
        'video': ['mp4', 'avi', 'mov', 'mkv', 'gif']
    }
    
    # Configurações do servidor
    HOST = '127.0.0.1'
    PORT = 8012 