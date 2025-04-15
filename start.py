#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path

def install_package(package, extra_args=None):
    """Instala um pacote específico"""
    try:
        cmd = [sys.executable, "-m", "pip", "install"]
        if extra_args:
            cmd.extend(extra_args)
        cmd.append(package)
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar {package}: {e}")
        return False

def check_dependencies():
    """Verifica se todas as dependências necessárias estão instaladas"""
    dependencies = [
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "python-multipart==0.0.9",
        "jinja2==3.1.3",
        "filetype==1.2.0",
        "ffmpeg-python==0.2.0"
    ]
    
    # Instala as dependências de build primeiro
    if platform.system() == "Windows":
        if not install_package("setuptools==69.1.1"):
            return False
        if not install_package("wheel==0.42.0"):
            return False
    
    # Instala cada dependência individualmente
    for dep in dependencies:
        if not install_package(dep):
            return False
    
    # Instala o Pillow separadamente com flags específicas para Windows
    if platform.system() == "Windows":
        # Tenta instalar o Pillow pré-compilado
        pillow_args = ["--only-binary=:all:", "--index-url=https://pypi.org/simple"]
        if not install_package("Pillow==11.2.1", pillow_args):
            # Se falhar, tenta com a versão anterior
            if not install_package("Pillow==11.1.0", pillow_args):
                # Se ainda falhar, tenta com a versão mais antiga disponível
                if not install_package("Pillow==10.4.0", pillow_args):
                    return False
    else:
        if not install_package("Pillow==11.2.1"):
            return False
    
    # Verifica se todas as dependências foram instaladas corretamente
    try:
        import fastapi
        import uvicorn
        import ffmpeg
        import PIL
        import filetype
        return True
    except ImportError as e:
        print(f"Erro ao verificar dependências: {e}")
        return False

def create_directories():
    """Cria os diretórios necessários se não existirem"""
    directories = [
        "app/static/uploads",
        "app/static/images",
        "app/templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Diretório verificado/criado: {directory}")

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("Erro: FFmpeg não encontrado!")
        if platform.system() == "Windows":
            print("Por favor, instale o FFmpeg manualmente e adicione ao PATH")
            print("Download: https://ffmpeg.org/download.html")
            print("Instruções:")
            print("1. Baixe o FFmpeg do site oficial")
            print("2. Extraia os arquivos para uma pasta (ex: C:\\ffmpeg)")
            print("3. Adicione a pasta bin ao PATH do sistema")
            print("4. Reinicie o terminal e tente novamente")
        else:
            print("Instalando FFmpeg...")
            if platform.system() == "Linux":
                subprocess.run(["sudo", "apt", "update"])
                subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["brew", "install", "ffmpeg"])
        return False

def main():
    """Função principal que inicia o sistema"""
    print("=" * 50)
    print("Iniciando TheSkullCon - File Converter")
    print("=" * 50)
    
    # Verifica dependências
    if not check_dependencies():
        print("Erro ao instalar dependências. Verifique as mensagens acima.")
        sys.exit(1)
    
    # Cria diretórios necessários
    create_directories()
    
    # Verifica FFmpeg
    if not check_ffmpeg():
        print("Erro: FFmpeg é necessário para o funcionamento do sistema")
        sys.exit(1)
    
    # Inicia o servidor
    print("\nIniciando servidor...")
    print("Acesse: http://localhost:8012")
    print("Pressione Ctrl+C para encerrar")
    print("=" * 50)
    
    try:
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8012, reload=True)
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
    except Exception as e:
        print(f"Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 