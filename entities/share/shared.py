from pydantic import BaseModel

class Person(BaseModel):
    first_name:str
    last_name:str

class Author(BaseModel):
    id:int|None=None
    value:str|None=None

class Cargo(BaseModel):
    id:int 
    value:str

class Member(BaseModel):
    id:int | None = None
    first_name:str 
    last_name:str 
    cargo:Cargo