from pydantic import BaseModel

class Trabajo(BaseModel):
    title:str | None = None
    course:str | None = None
    year:str | None = None
    link:str | None = None