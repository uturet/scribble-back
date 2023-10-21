
from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.models.posts import PostResponse
from app.db.actions import get_feed_result
from app.db import get_session
import time

router = APIRouter()

@router.get('/feed')
def feed_posts(page: int, db=Depends(get_session)) -> List[PostResponse]:
    """ Lists all posts of the current user """
    return [PostResponse(
            id=p.id,
            img=p.img,
            title=p.title,
            owner={
                "id": p.owner.id,
                "username": p.owner.username,
                "image": p.owner.image
            },
            created_at=time.time() * 1000
        ) for p in get_feed_result(page, db)]
