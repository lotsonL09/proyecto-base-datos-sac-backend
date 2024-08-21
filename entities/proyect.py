from pydantic import BaseModel
from datetime import datetime
from entities.shared import Person

class Period(BaseModel):
    year_start:datetime
    year_end:datetime

#Convenios
class Agreement(BaseModel):
    name:str

class Proyect(BaseModel):
    id: int |None =None
    name:str | None = None 
    coordinator:Person | None = None
    researches:list[Person] | None = None
    agreements:list[Agreement] | None = None
    status:str | None = None
    period:Period | None = None
