# Este arquivo é necessário para tornar o diretório app um pacote Python 

from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///theskullcon.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o banco de dados
    db.init_app(app)
    
    # Configura o login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registra os blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app 