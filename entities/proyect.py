from pydantic import BaseModel
from datetime import datetime
from entities.share.shared import Person

class Period(BaseModel):
    year_start:datetime |None =None
    year_end:datetime |None =None

#Convenios
class Agreement(BaseModel):
    name:str |None =None

class Proyect(BaseModel):
    id: int |None =None
    name:str | None = None 
    coordinator:Person | None = None
    researchers:list[Person] | None = None
    agreements:list[Agreement] | None = None
    status:int | None = None
    period:Period | None = None


class Proyect_db(BaseModel):
    id:int | None = None
    name:str | None = None
    id_coordinator: int | None = None
    id_status: int | None = None
    period: Period | None = None
