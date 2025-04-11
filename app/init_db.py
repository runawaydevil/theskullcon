from sqlalchemy.orm import Session
from . import database, models
from .auth import get_password_hash
from app import create_app, db
from app.models import User

def init_db(db: Session):
    # Cria o super admin se não existir
    admin = db.query(models.User).filter(models.User.email == "pablo@pablomurad.com").first()
    if not admin:
        admin = models.User(
            email="pablo@pablomurad.com",
            hashed_password=get_password_hash("Driver2136#"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("Super admin criado com sucesso!")
    else:
        print("Super admin já existe!")

def init_db_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Verifica se já existe um usuário administrador
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                is_admin=True,
                is_super_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Usuário administrador criado com sucesso!')
        else:
            print('Usuário administrador já existe.')

if __name__ == "__main__":
    db = next(database.get_db())
    init_db(db)
    init_db_app() 