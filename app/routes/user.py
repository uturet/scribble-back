from app.db import get_session
from app.db.actions import create_user, get_user_by_name
from app.exceptions import (InvalidPermissions, InvalidUserName,
                            UsernameAlreadyTaken)
from app.db.models import User
from app.models.user import UserCreate, UserResponse
from app.security import manager
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/user"
)


@router.post('/register', response_model=UserResponse, status_code=201)
def register(user: UserCreate, db=Depends(get_session)) -> UserResponse:
    """
    Registers a new user
    """
    try:
        user = create_user(user.username, user.password, db)
        return UserResponse.model_validate(user)
    except IntegrityError:
        raise UsernameAlreadyTaken
