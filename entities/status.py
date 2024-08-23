from pydantic import BaseModel

class Status(BaseModel):
    id:int
    value:str