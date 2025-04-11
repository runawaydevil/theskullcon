from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from . import routes

app = FastAPI(
    title="TheSkull.org - Conversor de Arquivos",
    description="""
    API para conversão de imagens e vídeos.
    - Imagens: Suporte para WebP, AVIF, JPEG XL, JPEG, PNG
    - Vídeos: Suporte para MP4, WebM, AVI, MKV (apenas super admin)
    """,
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de diretórios
UPLOAD_DIR = Path("uploads")
CONVERTED_DIR = Path("converted")
UPLOAD_DIR.mkdir(exist_ok=True)
CONVERTED_DIR.mkdir(exist_ok=True)

# Inclui as rotas
app.include_router(routes.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao TheSkull.org - API de Conversão de Arquivos",
        "docs": "/docs",
        "admin_email": "pablo@pablomurad.com"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 