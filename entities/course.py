from pydantic import BaseModel

class Course(BaseModel):
    id:int
    value:str