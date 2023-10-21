import datetime
from pydantic import ConfigDict, BaseModel


class PostBase(BaseModel):
    title: str
    data: list

    model_config = ConfigDict(from_attributes=True)


class PostUpdate(PostBase):
    id: int

class PostResponse(PostUpdate):
    created_at: datetime.datetime
    owner: str
