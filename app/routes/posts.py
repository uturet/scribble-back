from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.db import get_session
from app.db.actions import create_post, update_post, get_user_by_name, user_in_team
from app.exceptions import InvalidUserName
from app.models.posts import PostBase, PostUpdate, PostResponse
from app.db.models import Post
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
def update(post: PostUpdate, user=Depends(manager), db=Depends(get_session)) -> PostResponse:
    post_model = db.query(Post).where(Post.id == post.id).first()
    if post_model.owner_id == user.id or user_in_team(post_model, user):
        post = update_post(post_model, post, user, db)
        return PostResponse(
            id=post_model.id,
            title=post_model.title,
            data=post_model.data,
            owner=post_model.owner.username,
            created_at=post_model.created_at
        )


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
