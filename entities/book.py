from pydantic import BaseModel,PositiveInt
from entities.share.shared import Author

class Borrowed_to(BaseModel):
    first_name:str
    last_name:str

class Book(BaseModel):
    id:PositiveInt|None=None
    title:str | None = None
    authors:list[Author] | None = None
    location:PositiveInt | None = None
    status:PositiveInt | None = None
    borrowed_to:Borrowed_to | None = None
    amount:PositiveInt | None = None

class Book_update(BaseModel):
    id:PositiveInt|None=None
    title:str | None = None
    authors_added:list[Author] | None = None
    authors_deleted:list[Author] | None = None
    location:PositiveInt | None = None
    status:PositiveInt | None = None
    borrowed_to:Borrowed_to | None = None
    amount:PositiveInt | None = None


class Book_db(BaseModel):
    id_book:int|None=None
    id_title:int|None=None
    id_location:int|None=None
    id_status:int|None=None
    id_persona:int|None=None
