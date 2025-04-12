from PIL import Image
import os
import subprocess
import shutil
from app.config import Config

class VideoConverter:
    def __init__(self):
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS

    def is_allowed_file(self, filename):
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return ext in self.allowed_extensions['image'] + self.allowed_extensions['video']

    def is_image(self, filename):
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return ext in self.allowed_extensions['image']

    def is_video(self, filename):
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return ext in self.allowed_extensions['video']

    def convert_image(self, input_path, output_path, output_format):
        try:
            img = Image.open(input_path)
            img.save(output_path, format=output_format.upper())
            return True, "Conversão concluída com sucesso"
        except Exception as e:
            return False, f"Erro ao converter imagem: {str(e)}"

    def convert_video(self, input_path, output_path, output_format):
        try:
            # Verificar se o FFmpeg está instalado
            try:
                subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                return False, "FFmpeg não está instalado ou não está no PATH do sistema"

            # Criar diretório de saída se não existir
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            if output_format.lower() == 'gif':
                # Converter para GIF usando FFmpeg
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-vf', 'fps=10,scale=320:-1:flags=lanczos',
                    '-f', 'gif', output_path
                ]
            else:
                # Converter para outros formatos de vídeo
                cmd = [
                    'ffmpeg', '-i', input_path,
                    '-c:v', 'libx264', '-preset', 'medium',
                    '-c:a', 'aac', '-b:a', '128k',
                    output_path
                ]

            # Executar o comando FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Aguardar a conclusão do processo
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                return False, f"Erro ao converter vídeo: {stderr}"

            return True, "Conversão concluída com sucesso"
        except Exception as e:
            return False, f"Erro ao converter vídeo: {str(e)}"

    def convert(self, input_path, output_path, output_format):
        if not self.is_allowed_file(input_path):
            return False, "Tipo de arquivo não suportado"

        if self.is_image(input_path):
            return self.convert_image(input_path, output_path, output_format)
        elif self.is_video(input_path):
            return self.convert_video(input_path, output_path, output_format)
        else:
            return False, "Tipo de arquivo não reconhecido" 