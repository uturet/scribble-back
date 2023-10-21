
from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.exceptions import InvalidUserName
from app.models.posts import PostResponse
from app.security import manager

router = APIRouter(prefix='/')

@router.get('')
def list_posts(user=Depends(manager)) -> List[PostResponse]:
    """ Lists all posts of the current user """
    return [PostResponse.model_validate(p) for p in user.posts]