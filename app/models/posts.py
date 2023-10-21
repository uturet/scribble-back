import datetime
from pydantic import ConfigDict, BaseModel


class PostBase(BaseModel):
    title: str
    data: list

    model_config = ConfigDict(from_attributes=True)


class PostResponse(PostBase):
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
