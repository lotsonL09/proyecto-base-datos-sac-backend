from pydantic import BaseModel,PositiveInt
from entities.share.shared import Author
from entities.location import Location
from entities.status import Status
from entities.user import Role

class Borrowed_to(BaseModel):
    id:int | None = None
    user_name:str
    role:Role

#REFACTOR

class Book_Create(BaseModel):
    id:PositiveInt|None=None
    title:str | None = None
    authors:list[Author] | None = None
    location:Location | None = None
    status:Status | None = None
    borrowed_to: list[Borrowed_to] |str| None = None
    amount:PositiveInt | None = None


class Book_update(BaseModel):
    id:PositiveInt|None=None
    title:str | None = None
    authors_added:list[Author] | None = None
    authors_deleted:list[Author] | None = None
    location:Location | None = None
    status:Status | None = None
    borrowed_to_added:list[Borrowed_to] | None = None
    borrowed_to_deleted:list[Borrowed_to] | None = None
    amount:PositiveInt | None = None


class Book_db(BaseModel):
    id_book:int|None=None
    title:str|None=None
    id_location:int|None=None
    id_status:int|None=None
    amount:int|None=None


