from typing import List
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    image: str
    model_config = ConfigDict(from_attributes=True)


class LoginResponse(UserResponse):
    token: str
    token_type: str