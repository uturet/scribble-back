from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.db import get_session
from app.db.actions import get_comment_by_id, create_comment, get_comments_by_post_id
from app.models.comments import CommentBase, CommentResponse
from app.security import manager
from fastapi.exceptions import HTTPException

router = APIRouter(prefix='/comments')


@router.post('/create', response_model=CommentResponse)
def create(comment: CommentBase, user=Depends(manager), db=Depends(get_session)) -> CommentResponse:
    comment = create_comment(comment, user, db)
    return CommentResponse(
            id=comment.id,
            content=comment.content,
            post_id=comment.post_id,
            owner=user.username,
            created_at=comment.created_at
        )


@router.get('/list/{post_id}')
def list_comments_for_post(post_id: int, db=Depends(get_session)) -> List[CommentResponse]:
    """ Lists all comments of the given post """
    return [CommentResponse(
            id=cm.id,
            content=cm.content,
            post_id=cm.post_id,
            owner=cm.owner.username,
            created_at=cm.created_at
        ) for cm in get_comments_by_post_id(post_id, db)]


@router.delete('/{comment_id}', response_model=CommentResponse)
def delete(comment_id: int, user=Depends(manager), db=Depends(get_session)) -> CommentResponse:
    """ Delete comment """
    comment = get_comment_by_id(comment_id, db)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.owner.id != user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    db.delete(comment)
    db.commit()
    return CommentResponse(
            id=comment.id,
            content=comment.content,
            post_id=comment.post_id,
            owner=user.username,
            created_at=comment.created_at
        )
