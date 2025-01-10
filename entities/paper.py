from pydantic import BaseModel
from datetime import datetime
from entities.share.shared import Member

class Paper(BaseModel):
    id: int |None = None
    title:str | None = None
    link:str | None = None
    year:str | None = None
    members:list[Member] | None = None

class Paper_update(BaseModel):
    id: int |None = None
    title:str | None = None
    link:str | None = None
    year:str | None = None
    members_added:list[Member] | None = None
    members_deleted:list[Member] | None = None