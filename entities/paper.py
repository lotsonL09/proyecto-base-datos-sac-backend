from pydantic import BaseModel
from datetime import datetime
from entities.share.shared import Member

class Paper(BaseModel):
    id: int |None =None
    title:str | None = None
    link:str | None = None
    year:datetime | None = None
    members:list[Member] | None = None