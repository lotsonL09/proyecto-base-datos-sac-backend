from pydantic import BaseModel

class Trabajo(BaseModel):
    id: int |None =None
    title:str | None = None
    course:int | None = None
    year:str | None = None
    link:str | None = None