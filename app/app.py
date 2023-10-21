from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.posts import router as posts_router

from fastapi_socketio import SocketManager

app = FastAPI()
socket_manager = SocketManager(app=app, socketio_path='')

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)

from app.routes.socks import *