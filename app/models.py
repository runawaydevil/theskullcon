from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
import enum

class FileType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    conversions = relationship("Conversion", back_populates="user")

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
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