from sqlalchemy.orm import Session
from . import database, models
from .auth import get_password_hash

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

if __name__ == "__main__":
    db = next(database.get_db())
    init_db(db) 