from typing import List

from app.models.posts import PostResponse
from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    image: str
    model_config = ConfigDict(from_attributes=True)
