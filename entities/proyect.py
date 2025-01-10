from pydantic import BaseModel
from datetime import datetime
from entities.share.shared import Member
from entities.status import Status

class Period(BaseModel):
    year_start:str |None = None
    year_end:str |None = None

#Convenios
class Agreement(BaseModel):
    id:int | None =None
    value:str |None =None

class Proyect(BaseModel):
    id: int |None =None
    name:str | None = None 
    coordinator:Member | None = None
    researchers:list[Member] | None = None
    agreements:list[Agreement] | None = None
    status:Status | None = None
    period:Period | None = None


class Proyect_db(BaseModel):
    id:int | None = None
    name:str | None = None
    id_coordinator: int | None = None
    id_status: int | None = None
    period: Period | None = None

class Proyect_update(BaseModel):
    id: int |None =None
    name:str | None = None 
    coordinator:Member | None = None
    researchers_added:list[Member] | None = None
    researchers_deleted:list[Member] | None = None
    agreements_added:list[Agreement] | None = None
    agreements_deleted:list[Agreement] | None = None
    status:Status | None = None
    period:Period | None = None