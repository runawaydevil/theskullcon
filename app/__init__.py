"""
TheSkullCon - File Converter
A modern web application for converting images and videos.
"""

__version__ = "1.0.0"
__author__ = "Pablo Murad (RunawayDevil)"
__license__ = "MIT"

from app.config import Config
from app.services.converter import VideoConverter

# Inicializar o conversor globalmente
converter = VideoConverter()

# Configurações globais
config = Config

# Este arquivo é necessário para tornar o diretório app um pacote Python 