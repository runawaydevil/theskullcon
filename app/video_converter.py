from moviepy.editor import VideoFileClip
import ffmpeg
from pathlib import Path
from typing import Union, Optional
import os

class VideoConverter:
    def __init__(self, quality: int = 80):
        self.quality = quality
        self.MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB em bytes

    def check_file_size(self, file_path: Union[str, Path]) -> bool:
        """Verifica se o arquivo está dentro do limite de tamanho"""
        return os.path.getsize(file_path) <= self.MAX_FILE_SIZE

    def convert(self, 
               input_path: Union[str, Path], 
               output_path: Union[str, Path], 
               target_format: str,
               resolution: str = "720p") -> bool:
        """
        Converte um vídeo para o formato especificado
        Formatos suportados: mp4, webm, avi, mkv
        Resoluções: 480p, 720p, 1080p
        """
        try:
            if not self.check_file_size(input_path):
                raise ValueError("Arquivo excede o limite de 500MB")

            # Mapeia resoluções para dimensões
            resolutions = {
                "480p": (854, 480),
                "720p": (1280, 720),
                "1080p": (1920, 1080)
            }
            width, height = resolutions.get(resolution, (1280, 720))

            if target_format.lower() == "mp4":
                return self._convert_to_mp4(input_path, output_path, width, height)
            elif target_format.lower() == "webm":
                return self._convert_to_webm(input_path, output_path, width, height)
            elif target_format.lower() == "avi":
                return self._convert_to_avi(input_path, output_path, width, height)
            elif target_format.lower() == "mkv":
                return self._convert_to_mkv(input_path, output_path, width, height)
            else:
                raise ValueError(f"Formato não suportado: {target_format}")
        except Exception as e:
            print(f"Erro na conversão: {str(e)}")
            return False

    def _convert_to_mp4(self, input_path: Union[str, Path], output_path: Union[str, Path], width: int, height: int) -> bool:
        """Converte para MP4 com compressão H.264"""
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(stream, str(output_path), 
                             vcodec='libx264', 
                             acodec='aac', 
                             video_bitrate=f'{self.quality}k',
                             audio_bitrate='128k')
        ffmpeg.run(stream, overwrite_output=True)
        return True

    def _convert_to_webm(self, input_path: Union[str, Path], output_path: Union[str, Path], width: int, height: int) -> bool:
        """Converte para WebM com compressão VP9"""
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(stream, str(output_path), 
                             vcodec='libvpx-vp9', 
                             acodec='libopus',
                             video_bitrate=f'{self.quality}k',
                             audio_bitrate='128k')
        ffmpeg.run(stream, overwrite_output=True)
        return True

    def _convert_to_avi(self, input_path: Union[str, Path], output_path: Union[str, Path], width: int, height: int) -> bool:
        """Converte para AVI"""
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(stream, str(output_path), 
                             vcodec='mpeg4',
                             acodec='mp3',
                             video_bitrate=f'{self.quality}k',
                             audio_bitrate='128k')
        ffmpeg.run(stream, overwrite_output=True)
        return True

    def _convert_to_mkv(self, input_path: Union[str, Path], output_path: Union[str, Path], width: int, height: int) -> bool:
        """Converte para MKV com compressão H.264"""
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.filter(stream, 'scale', width, height)
        stream = ffmpeg.output(stream, str(output_path), 
                             vcodec='libx264',
                             acodec='aac',
                             video_bitrate=f'{self.quality}k',
                             audio_bitrate='128k')
        ffmpeg.run(stream, overwrite_output=True)
        return True 