from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.posts import router as posts_router
from fastapi_socketio import SocketManager

from typing import List
from fastapi.param_functions import Depends
from app.security import manager

app = FastAPI()
socket_manager = SocketManager(app=app, socketio_path='')

app.include_router(posts_router)
app.include_router(auth_router)
app.include_router(user_router)

from app.routes.socks import *
