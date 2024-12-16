"""Схема. Pylint говорит, что мало публичных методов, но больше и не требуется."""
from pydantic import BaseModel

class UserCreate(BaseModel):
    """Схема для создания пользователя"""
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    """Схема для создания поста"""
    title: str
    content: str
    user_id: int

class UserOut(BaseModel):
    """Схема для вывода информации о пользователе"""
    id: int
    username: str
    email: str

    class Config:
        """Класс конфигурации"""
        from_attributes = True

class PostOut(BaseModel):
    """Схема для вывода информации о постах"""
    id: int
    title: str
    content: str
    user_id: int
    user: UserOut

    class Config:
        """Класс конфигурации"""
        from_attributes = True
