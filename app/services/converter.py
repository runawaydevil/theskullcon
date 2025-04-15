from PIL import Image
import os
import subprocess
import shutil
from app.config import Config
import filetype

class VideoConverter:
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        self.max_content_length = Config.MAX_CONTENT_LENGTH

    def is_allowed_file(self, filename):
        """Check if file extension is allowed"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions['images'] or ext in self.allowed_extensions['videos']

    def is_image(self, filename):
        """Check if file is an image"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions['images']

    def is_video(self, filename):
        """Check if file is a video"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions['videos']

    def detect_file_type(self, file_path: str) -> str:
        """Detect file type using filetype"""
        try:
            kind = filetype.guess(file_path)
            if kind is None:
                # Fallback para extensão do arquivo
                ext = os.path.splitext(file_path)[1].lower()
                if ext in self.allowed_extensions['images']:
                    return 'image'
                elif ext in self.allowed_extensions['videos']:
                    return 'video'
                else:
                    raise ValueError("Could not determine file type")
                
            mime_type = kind.mime
            if mime_type.startswith('image/'):
                return 'image'
            elif mime_type.startswith('video/'):
                return 'video'
            elif mime_type.startswith('audio/'):
                return 'audio'
            else:
                raise ValueError(f"Unsupported file type: {mime_type}")
        except Exception as e:
            raise ValueError(f"Error detecting file type: {str(e)}")

    def convert(self, input_path: str, target_format: str) -> str:
        """
        Converte um arquivo para o formato especificado
        """
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(input_path):
                raise FileNotFoundError("File not found")

            # Verificar tamanho do arquivo
            file_size = os.path.getsize(input_path)
            if file_size > self.max_content_length:
                raise ValueError(f"File size exceeds maximum allowed size of {self.max_content_length} bytes")

            # Detectar o tipo do arquivo
            file_type = self.detect_file_type(input_path)

            # Verificar se o formato de saída é suportado
            if file_type == 'image' and target_format.lower() not in ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff']:
                raise ValueError(f"Unsupported image format: {target_format}")
            elif file_type == 'video' and target_format.lower() not in ['mp4', 'webm', 'avi']:
                raise ValueError(f"Unsupported video format: {target_format}")
            elif file_type == 'audio' and target_format.lower() not in ['mp3', 'wav', 'ogg']:
                raise ValueError(f"Unsupported audio format: {target_format}")

            # Gerar nome do arquivo de saída
            output_filename = os.path.splitext(os.path.basename(input_path))[0] + f".{target_format}"
            output_path = os.path.join(self.upload_folder, output_filename)

            # Converter baseado no tipo de arquivo
            if file_type == 'image':
                self._convert_image(input_path, output_path, target_format)
            elif file_type == 'video':
                self._convert_video(input_path, output_path, target_format)
            elif file_type == 'audio':
                self._convert_audio(input_path, output_path, target_format)
            else:
                raise ValueError(f"Unsupported conversion: {file_type} to {target_format}")

            return output_path

        except Exception as e:
            # Remover arquivo de saída em caso de erro
            if 'output_path' in locals() and os.path.exists(output_path):
                os.remove(output_path)
            raise e

    def _convert_image(self, input_path: str, output_path: str, output_format: str):
        """
        Converte uma imagem para o formato especificado
        """
        try:
            with Image.open(input_path) as img:
                if output_format.lower() == 'webp':
                    img.save(output_path, 'WEBP', quality=95, method=6)
                elif output_format.lower() in ['jpg', 'jpeg']:
                    img.save(output_path, 'JPEG', quality=95, optimize=True)
                elif output_format.lower() == 'png':
                    img.save(output_path, 'PNG', optimize=True)
                elif output_format.lower() == 'bmp':
                    img.save(output_path, 'BMP')
                elif output_format.lower() == 'tiff':
                    img.save(output_path, 'TIFF')
                else:
                    raise ValueError(f"Unsupported image format: {output_format}")
        except Exception as e:
            raise ValueError(f"Error converting image: {str(e)}")

    def _convert_video(self, input_path: str, output_path: str, output_format: str):
        """
        Converte um vídeo para o formato especificado
        """
        try:
            if output_format.lower() == 'mp4':
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:v', 'libx264', '-preset', 'medium',
                    '-c:a', 'aac', '-b:a', '128k',
                    output_path
                ]
            elif output_format.lower() == 'webm':
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:v', 'libvpx-vp9', '-crf', '30',
                    '-c:a', 'libopus', '-b:a', '128k',
                    output_path
                ]
            elif output_format.lower() == 'avi':
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:v', 'mpeg4', '-q:v', '3',
                    '-c:a', 'mp3', '-b:a', '128k',
                    output_path
                ]
            else:
                raise ValueError(f"Unsupported video format: {output_format}")

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise ValueError(f"FFmpeg error: {result.stderr}")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error converting video: {e.stderr}")
        except Exception as e:
            raise ValueError(f"Error converting video: {str(e)}")

    def _convert_audio(self, input_path: str, output_path: str, output_format: str):
        """
        Converte um áudio para o formato especificado
        """
        try:
            if output_format.lower() == 'mp3':
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:a', 'libmp3lame', '-b:a', '192k',
                    output_path
                ]
            elif output_format.lower() == 'wav':
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:a', 'pcm_s16le',
                    output_path
                ]
            elif output_format.lower() == 'ogg':
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:a', 'libvorbis', '-q:a', '4',
                    output_path
                ]
            else:
                raise ValueError(f"Unsupported audio format: {output_format}")

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise ValueError(f"FFmpeg error: {result.stderr}")
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error converting audio: {e.stderr}")
        except Exception as e:
            raise ValueError(f"Error converting audio: {str(e)}") 