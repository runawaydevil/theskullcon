# TheSkull.org - Conversor de Imagens

Um sistema de conversão de imagens com suporte a múltiplos formatos modernos, incluindo WebP, AVIF e JPEG XL.

## Características

- Conversão para múltiplos formatos (WebP, AVIF, JPEG XL, JPEG, PNG)
- Autenticação segura com JWT
- Interface RESTful API
- Armazenamento de histórico de conversões
- Suporte a compressão avançada
- Design responsivo

## Requisitos

- Python 3.8+
- PostgreSQL
- Bibliotecas Python (listadas em requirements.txt)

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

4. Configure o banco de dados:
```bash
# Crie o banco de dados PostgreSQL
createdb theskullcon

# Copie o arquivo .env.example para .env e configure as variáveis
cp .env.example .env
```

5. Execute as migrações do banco de dados:
```bash
alembic upgrade head
```

## Uso

1. Inicie o servidor:
```bash
python -m app.main
```

2. Acesse a API em `http://localhost:8000`

3. Use o endpoint `/docs` para acessar a documentação Swagger da API

## Endpoints Principais

- `POST /convert` - Converte uma imagem
- `POST /token` - Obtém token de autenticação
- `GET /users/me` - Informações do usuário atual
- `GET /conversions` - Histórico de conversões

## Segurança

- Todas as senhas são hashed usando bcrypt
- Autenticação via JWT
- Proteção contra CSRF
- Validação de tipos de arquivo
- Limite de tamanho de arquivo

## Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes. 