import datetime
from pydantic import ConfigDict, BaseModel
from fastapi import File


class PostBase(BaseModel):
    title: str
    img: str
    model_config = ConfigDict(from_attributes=True)


class PostUpdate(PostBase):
    id: int

class PostResponse(PostUpdate):
    created_at: float
    owner: str | dict
