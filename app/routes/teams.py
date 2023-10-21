from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.db import get_session
from app.db.actions import (
    get_user_by_id, 
    get_post_by_id
)
from app.models.teams import TeamBase, TeamResponse
from app.security import manager
from fastapi.exceptions import HTTPException
from app.models.user import UserResponse

router = APIRouter(prefix='/teams')


@router.post('/add', response_model=TeamResponse)
def create(team: TeamBase, user=Depends(manager), db=Depends(get_session)) -> TeamResponse:
    team_user = get_user_by_id(team.user_id, db)
    post = get_post_by_id(team.post_id, db)

    if user.id == team_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if not team_user or not post:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    post.users.append(team_user)
    db.commit()
    
    return TeamResponse(
            post_id=team.post_id,
            users=[
        UserResponse(id=u.id, username=u.username, image=u.image) for u in post.users
    ])


@router.get('/list/{post_id}', response_model=TeamResponse)
def list_comments_for_post(post_id: int, db=Depends(get_session)) -> TeamResponse:
    """ Lists all comments of the given post """
    post = get_post_by_id(post_id, db)
    
    if not post:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return TeamResponse(
            post_id=post_id,
            users=[
        UserResponse(id=u.id, username=u.username, image=u.image) for u in post.users
    ])


@router.delete('/{post_id}/{user_id}', response_model=bool)
def delete(post_id: int, user_id: int, user=Depends(manager), db=Depends(get_session)) -> TeamResponse:
    """ Delete comment """
    team_user = get_user_by_id(user_id, db)
    post = get_post_by_id(post_id, db)

    if user.id == team_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if (not team_user or not post) or \
        (post not in team_user.team_posts or team_user not in post.users):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    post.users.remove(team_user)
    db.commit()
    return True