from pydantic import BaseModel
from datetime import datetime
from entities.location import Location
from entities.status import Status

class Type(BaseModel):
    id:int | None = None
    value:str|None = None

class Equipment_Create(BaseModel):
    id:int | None = None
    equipment:str | None = None
    description:str | None = None
    evidence:str | None = None
    origin:str | None = None
    year:str | None = None
    type:Type | None = None
    location: Location | None = None
    status: Status | None = None
