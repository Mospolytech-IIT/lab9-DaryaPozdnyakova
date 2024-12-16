"""Лабораторная работа 9"""
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud
import models
import database

app = FastAPI()

# Шаблоны
templates = Jinja2Templates(directory="templates")

def get_db():
    """Настроиваем БД"""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=RedirectResponse)
def root():
    """Главная страница, всегда перенаправляет на список пользователей"""
    return RedirectResponse(url="/users")

@app.get("/users/", response_class=templates.TemplateResponse)
def get_users_page(request: Request, db: Session = Depends(get_db)):
    """Главная страница со списком всех пользователей"""
    users = crud.get_users(db)
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

@app.get("/users/new", response_class=templates.TemplateResponse)
def create_user_page(request: Request):
    """Создание нового пользователя"""
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/users/new")
def create_user_post(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Создание нового пользователя"""
    crud.create_user(db, username, email, password)
    return RedirectResponse(url="/users", status_code=303)

@app.get("/users/{user_id}/edit", response_class=templates.TemplateResponse)
def edit_user_page(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Отображение страницы редактирования данных пользователя"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})


@app.post("/users/{user_id}/edit")
def edit_user_post(
        user_id: int,
        new_email: str = Form(...),
        db: Session = Depends(get_db)
):
    """Обработчик обновления данных пользователя"""

    # Получаем пользователя из базы данных
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем данные пользователя, передаем имя, email и пароль
    user = crud.update_user(db, user_id, user.username, new_email, user.password)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return RedirectResponse(url="/users", status_code=303)

@app.post("/users/{user_id}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удаление пользователя"""
    if not crud.delete_user_and_posts(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(url="/users", status_code=303)

@app.get("/posts/", response_class=templates.TemplateResponse)
def get_posts_page(request: Request, db: Session = Depends(get_db)):
    """Страница всех постов"""
    posts = crud.get_posts(db)
    return templates.TemplateResponse("posts_list.html", {"request": request, "posts": posts})

@app.get("/posts/new", response_class=templates.TemplateResponse)
def create_post_page(request: Request):
    """Создание нового поста"""
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/new")
def create_post_post(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """Создание нового поста"""
    crud.create_post(db, title, content, user_id)
    return RedirectResponse(url="/posts", status_code=303)

@app.get("/posts/{post_id}/edit", response_class=templates.TemplateResponse)
def edit_post_page(request: Request, post_id: int, db: Session = Depends(get_db)):
    """Редактирование поста"""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@app.post("/posts/{post_id}/edit")
def edit_post_post(
    post_id: int,
    new_content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Редактирование поста"""
    crud.update_post_content(db, post_id, new_content)
    return RedirectResponse(url="/posts", status_code=303)

@app.post("/posts/{post_id}/delete")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удаление поста"""
    if not crud.delete_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return RedirectResponse(url="/posts", status_code=303)
