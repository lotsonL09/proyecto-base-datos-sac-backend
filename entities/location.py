from pydantic import BaseModel

class Location(BaseModel):
    id:int
    value:str