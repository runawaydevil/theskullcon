from PIL import Image
import os
import subprocess
import shutil
from app.config import Config
import filetype

class VideoConverter:
    def __init__(self):
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS

    def is_allowed_file(self, filename):
        """Check if file extension is allowed"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions['image'] or ext in self.allowed_extensions['video']

    def is_image(self, filename):
        """Check if file is an image"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions['image']

    def is_video(self, filename):
        """Check if file is a video"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions['video']

    def detect_file_type(self, file_path: str) -> str:
        """Detect file type using filetype"""
        kind = filetype.guess(file_path)
        if kind is None:
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

    def convert_file(self, file_path: str, output_format: str) -> str:
        """Convert file to specified format"""
        file_type = self.detect_file_type(file_path)
        
        # Get output filename
        output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}.{output_format}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        if file_type == 'image':
            return self.convert_image(file_path, output_path, output_format)
        elif file_type == 'video':
            return self.convert_video(file_path, output_path, output_format)
        elif file_type == 'audio':
            return self.convert_audio(file_path, output_path, output_format)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def convert_image(self, input_path: str, output_path: str, output_format: str) -> str:
        """Convert image to specified format"""
        try:
            with Image.open(input_path) as img:
                img.save(output_path, format=output_format.upper())
            os.remove(input_path)  # Remove original file
            return os.path.basename(output_path)
        except Exception as e:
            raise Exception(f"Error converting image: {str(e)}")

    def convert_video(self, input_path: str, output_path: str, output_format: str) -> str:
        """Convert video to specified format using FFmpeg"""
        try:
            # Check if FFmpeg is installed
            try:
                subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                raise Exception("FFmpeg is not installed or not in PATH")

            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Build FFmpeg command
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', 'libx264' if output_format in ['mp4', 'mkv'] else 'copy',
                '-c:a', 'aac' if output_format in ['mp4', 'mkv'] else 'copy',
                '-y', output_path
            ]

            # Run FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Wait for process to complete
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {stderr}")

            os.remove(input_path)  # Remove original file
            return os.path.basename(output_path)

        except Exception as e:
            raise Exception(f"Error converting video: {str(e)}")

    def convert_audio(self, input_path: str, output_path: str, output_format: str) -> str:
        """Convert audio to specified format using FFmpeg"""
        try:
            # Check if FFmpeg is installed
            try:
                subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                raise Exception("FFmpeg is not installed or not in PATH")

            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Build FFmpeg command
            cmd = [
                'ffmpeg', '-i', input_path,
                '-vn',  # No video
                '-y', output_path
            ]

            # Run FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Wait for process to complete
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {stderr}")

            os.remove(input_path)  # Remove original file
            return os.path.basename(output_path)

        except Exception as e:
            raise Exception(f"Error converting audio: {str(e)}")

    def convert(self, input_path, output_path, output_format):
        """Convert file to specified format"""
        try:
            # Get file type
            kind = filetype.guess(input_path)
            if kind is None:
                raise ValueError("Could not determine file type")
                
            mime_type = kind.mime
            
            if mime_type.startswith('image/'):
                return self.convert_image(input_path, output_path, output_format)
            elif mime_type.startswith('video/'):
                return self.convert_video(input_path, output_path, output_format)
            else:
                raise ValueError(f"Unsupported file type: {mime_type}")
                
        except Exception as e:
            raise Exception(f"Error converting file: {str(e)}") 