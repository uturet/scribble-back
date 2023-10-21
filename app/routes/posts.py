from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.db import get_session
from app.db.actions import create_post, update_post, get_user_by_name, user_in_team
from app.exceptions import InvalidUserName
from app.models.posts import PostBase, PostResponse
from app.security import manager

router = APIRouter(prefix='/posts')


@router.post('/create', response_model=PostResponse)
def create(post: PostBase, user=Depends(manager), db=Depends(get_session)) -> PostResponse:
    post = create_post(post, user, db)
    return PostResponse.model_validate(post)


@router.put('/update', responses={
        200: {"model": PostResponse},
        401: {
            "description": "Unauthorized user!",
        }},
        response_model=PostResponse)
def update(post: PostBase, user=Depends(manager), db=Depends(get_session)) -> PostResponse:
    if post.user_id == user.id or user_in_team(post, user):
        post = update_post(post, user, db)
        return PostResponse.model_validate(post)


@router.get('/list')
def list_posts(user=Depends(manager)) -> List[PostResponse]:
    """ Lists all posts of the current user """
    return [PostResponse.model_validate(p) for p in user.posts]


@router.get('/list/{username}')
def list_posts_for_user(username: str, _=Depends(manager), db=Depends(get_session)) -> List[PostResponse]:
    """ Lists all posts of the given user """
    user = get_user_by_name(username, db)

    if user is None:
        raise InvalidUserName

    return [PostResponse.model_validate(p) for p in user.posts]
