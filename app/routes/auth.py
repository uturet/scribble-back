from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from app.db import get_session
from app.db.actions import get_user_by_name
from app.models.user import LoginResponse
from app.security import verify_password, manager
from datetime import timedelta


router = APIRouter(
    prefix="/auth"
)

@router.post('/login', response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)) -> LoginResponse:
    """
    Logs in the user provided by form_data.username and form_data.password
    """
    user = get_user_by_name(form_data.username, db)
    if user is None:
        raise InvalidCredentialsException

    if not verify_password(form_data.password, user.password):
        raise InvalidCredentialsException

    token = manager.create_access_token(
        data={'sub': user.username}, 
        expires=timedelta(days=4))
    return LoginResponse(
        id=user.id,
        username=user.username,
        image=user.image,
        token=token,
        token_type='bearer'
    )
