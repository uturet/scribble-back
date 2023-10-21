
from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.models.posts import PostResponse
from app.db.actions import get_feed_result
from app.db import get_session

router = APIRouter()

@router.get('/')
def feed_posts(page: int, db=Depends(get_session)) -> List[PostResponse]:
    """ Lists all posts of the current user """
    return [PostResponse(
            id=p.id,
            title=p.title,
            data=p.data,
            owner=p.owner.username,
            created_at=p.created_at
        ) for p in get_feed_result(page, db)]

