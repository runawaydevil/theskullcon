from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import timedelta
import time
from pathlib import Path
import shutil

from . import auth, database, models, image_converter, video_converter
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import FileType

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verifica se é o super admin
    if form_data.username != "pablo@pablomurad.com" or form_data.password != "Driver2136#":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/convert/image")
async def convert_image(
    file: UploadFile = File(...),
    target_format: str = "webp",
    quality: int = 80,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    """
    Converte uma imagem para o formato especificado
    Formatos suportados: webp, avif, jpegxl, jpg, png
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem")
    
    # Cria diretórios se não existirem
    UPLOAD_DIR = Path("uploads")
    CONVERTED_DIR = Path("converted")
    UPLOAD_DIR.mkdir(exist_ok=True)
    CONVERTED_DIR.mkdir(exist_ok=True)
    
    # Salva o arquivo temporariamente
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Obtém o tamanho original do arquivo
    file_size_before = os.path.getsize(file_path)
    
    # Gera nome do arquivo convertido
    original_format = file.filename.split('.')[-1].lower()
    converted_filename = f"{file.filename.rsplit('.', 1)[0]}.{target_format}"
    converted_path = CONVERTED_DIR / converted_filename
    
    # Inicia a conversão
    start_time = time.time()
    converter = image_converter.ImageConverter(quality=quality)
    success = converter.convert(file_path, converted_path, target_format)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erro na conversão da imagem")
    
    # Calcula o tempo de conversão
    conversion_time = int((time.time() - start_time) * 1000)  # em milissegundos
    
    # Obtém o tamanho do arquivo convertido
    file_size_after = os.path.getsize(converted_path)
    
    # Salva a conversão no banco de dados
    conversion = models.Conversion(
        user_id=current_user.id,
        file_type=FileType.IMAGE,
        original_filename=file.filename,
        original_format=original_format,
        target_format=target_format,
        file_size_before=file_size_before,
        file_size_after=file_size_after,
        conversion_time=conversion_time
    )
    db.add(conversion)
    db.commit()
    
    # Retorna informações sobre a conversão
    return {
        "message": "Conversão realizada com sucesso",
        "original_filename": file.filename,
        "converted_filename": converted_filename,
        "original_size": file_size_before,
        "converted_size": file_size_after,
        "compression_ratio": f"{((file_size_before - file_size_after) / file_size_before * 100):.2f}%",
        "conversion_time_ms": conversion_time
    }

@router.post("/convert/video")
async def convert_video(
    file: UploadFile = File(...),
    target_format: str = "mp4",
    quality: int = 80,
    resolution: str = "720p",
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    """
    Converte um vídeo para o formato especificado (apenas para super admin)
    Formatos suportados: mp4, webm, avi, mkv
    Resoluções: 480p, 720p, 1080p
    """
    # Verifica se é super admin
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas super administradores podem converter vídeos"
        )
    
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Arquivo não é um vídeo")
    
    # Cria diretórios se não existirem
    UPLOAD_DIR = Path("uploads")
    CONVERTED_DIR = Path("converted")
    UPLOAD_DIR.mkdir(exist_ok=True)
    CONVERTED_DIR.mkdir(exist_ok=True)
    
    # Salva o arquivo temporariamente
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Verifica o tamanho do arquivo
    file_size_before = os.path.getsize(file_path)
    if file_size_before > 500 * 1024 * 1024:  # 500MB
        os.remove(file_path)
        raise HTTPException(
            status_code=400, 
            detail="Arquivo excede o limite de 500MB"
        )
    
    # Gera nome do arquivo convertido
    original_format = file.filename.split('.')[-1].lower()
    converted_filename = f"{file.filename.rsplit('.', 1)[0]}.{target_format}"
    converted_path = CONVERTED_DIR / converted_filename
    
    # Inicia a conversão
    start_time = time.time()
    converter = video_converter.VideoConverter(quality=quality)
    success = converter.convert(file_path, converted_path, target_format, resolution)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erro na conversão do vídeo")
    
    # Calcula o tempo de conversão
    conversion_time = int((time.time() - start_time) * 1000)  # em milissegundos
    
    # Obtém o tamanho do arquivo convertido
    file_size_after = os.path.getsize(converted_path)
    
    # Salva a conversão no banco de dados
    conversion = models.Conversion(
        user_id=current_user.id,
        file_type=FileType.VIDEO,
        original_filename=file.filename,
        original_format=original_format,
        target_format=target_format,
        resolution=resolution,
        file_size_before=file_size_before,
        file_size_after=file_size_after,
        conversion_time=conversion_time
    )
    db.add(conversion)
    db.commit()
    
    # Retorna informações sobre a conversão
    return {
        "message": "Conversão realizada com sucesso",
        "original_filename": file.filename,
        "converted_filename": converted_filename,
        "resolution": resolution,
        "original_size": file_size_before,
        "converted_size": file_size_after,
        "compression_ratio": f"{((file_size_before - file_size_after) / file_size_before * 100):.2f}%",
        "conversion_time_ms": conversion_time
    }

@router.get("/conversions")
async def get_conversions(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(database.get_db)
):
    """
    Retorna o histórico de conversões do usuário
    """
    conversions = db.query(models.Conversion).filter(
        models.Conversion.user_id == current_user.id
    ).order_by(models.Conversion.created_at.desc()).all()
    
    return conversions 