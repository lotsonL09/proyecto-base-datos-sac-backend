from pydantic import BaseModel,PositiveInt
from entities.share.shared import Author
from entities.location import Location
from entities.status import Status

class Borrowed_to(BaseModel):
    id:int | None = None
    first_name:str
    last_name:str

class Title(BaseModel):
    id: int | None = None
    value: str | None = None

#REFACTOR

class Book_Create(BaseModel):
    id:PositiveInt|None=None
    title:Title | None = None
    authors:list[Author] | None = None
    location:Location | None = None
    status:Status | None = None
    borrowed_to: Borrowed_to | str | None = None
    amount:PositiveInt | None = None


class Book_update(BaseModel):
    id:PositiveInt|None=None
    title:Title | None = None
    authors_added:list[Author] | None = None
    authors_deleted:list[Author] | None = None
    location:Location | None = None
    status:Status | None = None
    borrowed_to:Borrowed_to | None = None
    amount:PositiveInt | None = None


class Book_db(BaseModel):
    id_book:int|None=None
    id_title:int|None=None
    id_location:int|None=None
    id_status:int|None=None
    id_persona:int|None=None


