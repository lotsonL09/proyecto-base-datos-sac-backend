from pydantic import BaseModel

class Person(BaseModel):
    first_name:str
    last_name:str

class Author(BaseModel):
    name:str

class Member(BaseModel):
    first_name:str
    last_name:str