from pydantic import BaseModel
from datetime import datetime

class Equipment(BaseModel):
    id:int | None = None
    equipment:str | None = None
    description:str | None = None
    image:str | None = None #modify later 
    location:str | None = None
    status:str | None = None
    type:str | None = None
    date:datetime | None = None
