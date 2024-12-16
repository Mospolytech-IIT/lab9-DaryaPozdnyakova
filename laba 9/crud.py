"""Методы CRUD"""
from sqlalchemy.orm import Session
from models import User, Post

def create_user(db: Session, username: str, email: str, password: str):
    """Функция для создания пользователя"""
    db_user = User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    """Функция для получения всех пользователей"""
    return db.query(User).all()

def create_post(db: Session, title: str, content: str, user_id: int):
    """Функция для создания поста"""
    db_post = Post(title=title, content=content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session):
    """Функция для получения всех постов"""
    return db.query(Post).all()

def get_posts_by_user(db: Session, user_id: int):
    """Функция для получения постов конкретного пользователя"""
    return db.query(Post).filter(Post.user_id == user_id).all()

def update_user(db: Session, user_id: int, username: str, email: str, password: str):
    """Функция для обновления данных пользователя (username, email, password)"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = username
        user.email = email
        user.password = password  # В реальных приложениях пароль следует хешировать
        db.commit()
        db.refresh(user)
        return user
    return None

def update_post_content(db: Session, post_id: int, new_content: str):
    """Функция для обновления content поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()
        db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    """Функция для удаления поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

def delete_user_and_posts(db: Session, user_id: int):
    """Функция для удаления пользователя и всех его постов"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # Удаляем все посты пользователя
        db.query(Post).filter(Post.user_id == user_id).delete()
        db.delete(user)
        db.commit()
        return True
    return False
