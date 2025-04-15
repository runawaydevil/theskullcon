from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import os
import time
import asyncio
from app.services.converter import VideoConverter
from app.config import Config

app = FastAPI()

# Configuração de diretórios
app.mount("/static", StaticFiles(directory=Config.STATIC_FOLDER), name="static")
templates = Jinja2Templates(directory=Config.TEMPLATES_FOLDER)

# Criar diretórios necessários
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.STATIC_FOLDER, exist_ok=True)

# Inicializar o conversor
converter = VideoConverter()

async def cleanup_old_files():
    """Remove arquivos antigos do diretório de upload"""
    while True:
        try:
            current_time = time.time()
            for filename in os.listdir(Config.UPLOAD_FOLDER):
                file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)
                    if current_time - file_time > Config.CLEANUP_INTERVAL:
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Error removing file {filename}: {str(e)}")
        except Exception as e:
            print(f"Error in cleanup task: {str(e)}")
        await asyncio.sleep(Config.CLEANUP_INTERVAL)

@app.on_event("startup")
async def startup_event():
    """Inicializa a tarefa de limpeza de arquivos antigos"""
    asyncio.create_task(cleanup_old_files())

@app.get("/")
async def home(request: Request):
    """Página inicial"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    """Converte um arquivo para o formato especificado"""
    try:
        # Verificar se o arquivo foi enviado
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Verificar se o formato de destino foi especificado
        if not target_format:
            raise HTTPException(status_code=400, detail="Target format not specified")

        # Verificar se o arquivo é permitido
        if not converter.is_allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="File type not allowed")

        # Salvar arquivo temporariamente
        file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        try:
            # Converter arquivo
            output_path = converter.convert(file_path, target_format)

            # Retornar arquivo convertido
            return FileResponse(
                output_path,
                filename=os.path.basename(output_path),
                media_type=f"application/{target_format}"
            )
        finally:
            # Remover arquivo temporário
            if os.path.exists(file_path):
                os.remove(file_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    ) 