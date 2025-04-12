from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.services.converter import VideoConverter
from app.config import Config
import os
import shutil
from pathlib import Path

app = FastAPI()

# Configuração dos templates
templates = Jinja2Templates(directory="app/templates")

# Configuração dos arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Criar diretório de uploads se não existir
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Inicializar o conversor
converter = VideoConverter()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_file(
    request: Request,
    file: UploadFile = File(...),
    output_format: str = Form(...)
):
    try:
        # Verificar se o arquivo foi enviado
        if not file:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Nenhum arquivo foi enviado"
                }
            )

        # Verificar se o formato de saída é válido
        if not output_format:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Formato de saída não especificado"
                }
            )

        # Salvar o arquivo temporariamente
        file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Gerar nome do arquivo de saída
        output_filename = f"{Path(file.filename).stem}.{output_format}"
        output_path = os.path.join(Config.UPLOAD_FOLDER, output_filename)
        
        # Converter o arquivo
        success, message = converter.convert(file_path, output_path, output_format)
        
        # Limpar o arquivo temporário
        os.remove(file_path)
        
        if success:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "message": "Conversão concluída com sucesso!",
                    "output_file": output_filename
                }
            )
        else:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": message
                }
            )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Erro durante a conversão: {str(e)}"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 