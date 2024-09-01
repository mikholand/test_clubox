"""Основной файл приложения FastAPI (бэкенд) для работы Telegram Mini App."""
from db.database import lifespan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import profile, user

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user.router, prefix='/user')
app.include_router(profile.router, prefix='/profile')
