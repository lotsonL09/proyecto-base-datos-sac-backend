from pydantic import BaseModel
from entities.shared import Person

class Borrowed_to(BaseModel):
    first_name:str
    last_name:str

class Book(BaseModel):
    title:str | None = None
    author:Person | None = None
    location:str | None = None
    status:str | None = None
    borrowed_to:Borrowed_to | None = None
