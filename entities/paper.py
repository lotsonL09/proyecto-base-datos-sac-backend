from pydantic import BaseModel
from datetime import datetime
from entities.shared import Person

class Paper(BaseModel):
    id: int |None =None
    title:str | None = None
    link:str | None = None
    date:datetime | None = None
    authors:list[Person] | None = None