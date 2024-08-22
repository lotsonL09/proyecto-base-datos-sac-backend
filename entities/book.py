from pydantic import BaseModel,PositiveInt

class Author(BaseModel):
    name:str

class Borrowed_to(BaseModel):
    first_name:str
    last_name:str

class Book(BaseModel):
    id:int|None=None
    title:str | None = None
    author:list[Author] | None = None
    location:str | None = None
    status:str | None = None
    borrowed_to:Borrowed_to | None = None
    amount:PositiveInt | None = None


class Book_db(BaseModel):
    id_book:int|None=None
    id_title:int|None=None
    id_location:int|None=None
    id_status:int|None=None
    id_persona:int|None=None
