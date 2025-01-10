from pydantic import BaseModel

class Course(BaseModel):
    id:int
    value:str

class Trabajo(BaseModel):
    id: int |None =None
    title:str | None = None
    course:Course | None = None
    year:str | None = None
    link:str | None = None