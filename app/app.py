from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.feed import router as feed_router
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.posts import router as posts_router
from app.routes.comments import router as comments_router
from app.routes.teams import router as teams_router
from fastapi_socketio import SocketManager

from typing import List
from fastapi.param_functions import Depends
from app.security import manager

app = FastAPI()
socket_manager = SocketManager(app=app, socketio_path='')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feed_router)
app.include_router(teams_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(auth_router)
app.include_router(user_router)

from app.routes.socks import *
