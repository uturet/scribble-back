from typing import List
from fastapi import APIRouter, Form
from fastapi.param_functions import Depends
from app.db import get_session
from app.db.actions import create_post, update_post, get_user_by_id, user_in_team
from app.exceptions import InvalidUserName
from app.models.posts import PostBase, PostUpdate, PostResponse
from app.db.models import Post
from pydantic import BaseModel
from app.security import manager
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import string
import random
import base64
import time 
router = APIRouter(prefix='/posts')

def rund_name():
    return f"{''.join(random.choices(string.ascii_letters, k=25))}.png"

class Base(BaseModel):
    title: str

@router.post('/upload-file', response_model=str)
def upload_file(file: Annotated[bytes, File()],  user=Depends(manager), db=Depends(get_session)) -> str:
    image = base64.b64decode(file)
    name = rund_name()
    with open(f"public/{name}", 'wb') as f:
        f.write(image)
    return name

@router.post('/create', response_model=PostResponse)
def create(post: PostBase,  user=Depends(manager), db=Depends(get_session)) -> PostResponse:
    post = create_post(post, user, db)
    return PostResponse(
            id=post.id,
            img=post.img,
            title=post.title,
            owner=user.username,
            created_at=time.time() * 1000
        )


@router.put('/update', responses={
        200: {"model": PostResponse},
        401: {
            "description": "Unauthorized user!",
        }},
        response_model=PostResponse)
def update(post: PostUpdate, user=Depends(manager), db=Depends(get_session)) -> PostResponse:
    post_model = db.query(Post).where(Post.id == post.id).first()
    if post_model.owner_id == user.id or user_in_team(post_model, user):
        post = update_post(post_model, post, user, db)
        return PostResponse(
            id=post_model.id,
            img=post_model.img,
            title=post_model.title,
            owner=post_model.owner.username,
            created_at=time.time() * 1000
        )


@router.get('/list')
def list_posts(user=Depends(manager)) -> List[PostResponse]:
    """ Lists all posts of the current user """
    return [PostResponse(
            id=p.id,
            title=p.title,
            img=p.img,
            owner=user.username,
            created_at=time.time() * 1000
        ) for p in user.own_posts]


@router.get('/list/{user_id}')
def list_posts_for_user(user_id: int, db=Depends(get_session)) -> List[PostResponse]:
    """ Lists all posts of the given user """
    user = get_user_by_id(user_id, db)

    if user is None:
        raise InvalidUserName

    return [PostResponse(
            id=p.id,
            title=p.title,
            img=p.img,
            owner=user.username,
            created_at=time.time() * 1000
        ) for p in user.own_posts]
