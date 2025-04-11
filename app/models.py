from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timedelta
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class FileType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    conversions = relationship("Conversion", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin
        }

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String, nullable=False)  # Endereço IP do usuário
    file_type = Column(Enum(FileType), nullable=False)
    original_filename = Column(String)
    original_format = Column(String)
    target_format = Column(String)
    resolution = Column(String, nullable=True)  # Para vídeos
    file_size_before = Column(Integer)
    file_size_after = Column(Integer)
    conversion_time = Column(Integer)  # em milissegundos
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversions")

    @staticmethod
    def get_daily_conversions_count(db: 'Session', ip_address: str) -> int:
        """Retorna o número de conversões feitas por um IP nas últimas 24 horas"""
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        return db.query(func.count(Conversion.id)).filter(
            Conversion.ip_address == ip_address,
            Conversion.created_at >= twenty_four_hours_ago
        ).scalar() 