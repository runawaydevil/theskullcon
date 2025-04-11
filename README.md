# TheSkull.org - Conversor de Arquivos

API para conversão de imagens e vídeos com interface web moderna e responsiva.

## Funcionalidades

- **Conversão de Imagens**:
  - Suporte para WebP, AVIF, JPEG XL, JPEG, PNG
  - Controle de qualidade
  - Redimensionamento automático

- **Conversão de Vídeos** (apenas super admin):
  - Suporte para MP4, WebM, AVI, MKV
  - Compressão otimizada
  - Controle de resolução

- **Interface Web**:
  - Design moderno e responsivo
  - Upload via drag-and-drop
  - Preview de arquivos
  - Histórico de conversões

## Tecnologias Utilizadas

- **Backend**:
  - FastAPI
  - SQLAlchemy
  - Alembic
  - FFmpeg
  - Pillow

- **Frontend**:
  - Bootstrap 5
  - Font Awesome
  - Dropzone.js
  - Jinja2 Templates

## Requisitos

- Python 3.8+
- PostgreSQL
- FFmpeg
- Dependências Python (ver `requirements.txt`)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/theskullcon.git
cd theskullcon
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicialize o banco de dados:
```bash
alembic upgrade head
python -m app.init_db
```

## Executando o Projeto

1. Inicie o servidor:
```bash
python -m app.main
```

2. Acesse a aplicação:
```
http://localhost:8012
```

## Estrutura do Projeto

```
theskullcon/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── image_converter.py
│   ├── video_converter.py
│   ├── init_db.py
│   └── templates/
│       ├── base.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── converter/
│           └── index.html
├── alembic/
│   └── versions/
├── uploads/
├── converted/
├── requirements.txt
├── .env.example
└── README.md
```

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=postgresql://usuario:senha@localhost/theskullcon
SECRET_KEY=sua-chave-secreta
```

### Permissões de Usuário

- **Usuário Normal**: Pode converter imagens
- **Admin**: Pode converter imagens e vídeos
- **Super Admin**: Acesso total ao sistema

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 