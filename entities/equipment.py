from pydantic import BaseModel
from datetime import datetime

class Equipment(BaseModel):
    id:int | None = None
    equipment:str | None = None
    description:str | None = None
    evidence:str | None = None
    origin:str | None = None
    year:datetime | None = None
    type:str | None = None
    location:int | None = None
    status:int | None = None

class Equipment_Mongo(BaseModel):
    id:int | None = None
    equipment:str | None = None
    description:str | None = None
    evidence:str | None = None
    origin:str | None = None
    year: str | None = None
    type:str | None = None
    location: str | None = None
    status: str | None = None

