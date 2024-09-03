from pydantic import BaseModel

class Person(BaseModel):
    first_name:str
    last_name:str

class Author(BaseModel):
    id:int|None=None
    name:str|None=None

class Member(BaseModel):
    id:int | None = None
    first_name:str 
    last_name:str 