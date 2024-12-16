"""Настройка БД"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///D:/ВУЗ/ВУЗ 2024-2025/BackEnd/laba 9/delete.db"

# Создание движка
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

def get_db():
    """Функция для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
