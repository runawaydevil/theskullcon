from PIL import Image
import cv2
import numpy as np
import webp
import avif
import jpegxl
from pathlib import Path
from typing import Union, Optional
import io

class ImageConverter:
    def __init__(self, quality: int = 80):
        self.quality = quality

    def convert(self, 
               input_path: Union[str, Path], 
               output_path: Union[str, Path], 
               target_format: str) -> bool:
        """
        Converte uma imagem para o formato especificado
        """
        try:
            if target_format.lower() == "webp":
                return self._convert_to_webp(input_path, output_path)
            elif target_format.lower() == "avif":
                return self._convert_to_avif(input_path, output_path)
            elif target_format.lower() == "jpegxl":
                return self._convert_to_jpegxl(input_path, output_path)
            elif target_format.lower() in ["jpg", "jpeg"]:
                return self._convert_to_jpeg(input_path, output_path)
            elif target_format.lower() == "png":
                return self._convert_to_png(input_path, output_path)
            else:
                raise ValueError(f"Formato não suportado: {target_format}")
        except Exception as e:
            print(f"Erro na conversão: {str(e)}")
            return False

    def _convert_to_webp(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Converte para WebP com compressão avançada"""
        img = Image.open(input_path)
        img.save(output_path, "WEBP", quality=self.quality, method=6)
        return True

    def _convert_to_avif(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Converte para AVIF com alta compressão"""
        img = cv2.imread(str(input_path))
        if img is None:
            raise ValueError("Não foi possível ler a imagem")
        
        # Converte para RGB (AVIF trabalha com RGB)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Salva como AVIF
        avif.save(output_path, img_rgb, quality=self.quality)
        return True

    def _convert_to_jpegxl(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Converte para JPEG XL com compressão avançada"""
        img = Image.open(input_path)
        img.save(output_path, "JPEG XL", quality=self.quality)
        return True

    def _convert_to_jpeg(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Converte para JPEG com otimização"""
        img = Image.open(input_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output_path, "JPEG", quality=self.quality, optimize=True)
        return True

    def _convert_to_png(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> bool:
        """Converte para PNG com otimização"""
        img = Image.open(input_path)
        img.save(output_path, "PNG", optimize=True)
        return True 