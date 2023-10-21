from typing import Callable, Iterator, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
import json
from fastapi.exceptions import HTTPException
from app.db import get_session
from app.db.models import Post, User
from app.models.posts import PostBase
from app.security import hash_password, manager

@manager.user_loader(session_provider=get_session)
def get_user_by_name(
    name: str,
    db: Optional[Session] = None,
    session_provider: Callable[[], Iterator[Session]] = None
) -> Optional[User]:
    """
    Queries the database for a user with the given name

    Args:
        name: The name of the user
        db: The currently active database session
        session_provider: Optional method to retrieve a session if db is None (provided by our LoginManager)

    Returns:
        The user object or none
    """

    if db is None and session_provider is None:
        raise ValueError("db and session_provider cannot both be None.")

    if db is None:
        db = next(session_provider())

    user = db.query(User).where(User.username == name).first()
    return user


def create_user(name: str, password: str, db: Session) -> User:
    """
    Creates and commits a new user object to the database

    Args:
        name: The name of the user
        password: The plaintext password
        db: The active db session

    Returns:
        The newly created user.
    """
    hashed_pw = hash_password(password)
    user = User(username=name, password=hashed_pw)
    db.add(user)
    db.commit()
    return user


def create_post(post: PostBase, owner: User, db: Session) -> Post:
    post = Post(title=post.title, data=post.data, owner_id=owner.id)
    db.add(post)
    db.commit()
    return post


def update_post(post_model: Post, post: Post, owner: User, db: Session, session_provider=get_session) -> Post:
    if db is None and session_provider is None:
        raise ValueError("db and session_provider cannot both be None.")

    if db is None:
        db = next(session_provider())

    post_model.title = post.title
    post_model.data = post.data
    db.add(post_model)
    db.commit()


def user_in_team(post: Post, user: User, session_provider=get_session) -> bool:
    if db is None and session_provider is None:
        raise ValueError("db and session_provider cannot both be None.")

    if db is None:
        db = next(session_provider())

    post_team = [u.id for u in post.users]
    if user.id not in post_team:
        raise HTTPException(401)
    return True