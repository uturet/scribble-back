import datetime
from pydantic import ConfigDict, BaseModel


class CommentBase(BaseModel):
    content: str
    post_id: int

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(CommentBase):
    id: int
    created_at: float
    owner: str
