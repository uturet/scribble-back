from pydantic import ConfigDict, BaseModel

class TeamBase(BaseModel):
    user_id: int
    post_id: int

    model_config = ConfigDict(from_attributes=True)

class TeamResponse(BaseModel):
    post_id: int
    users: list
