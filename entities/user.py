from pydantic import BaseModel
from enum import Enum

class User(BaseModel):
    id: int |None =None
    user_name:str | None = None
    first_name:str | None = None
    last_name:str | None = None
    email:str | None = None
    category:str | None = None
    phone:str | None = None
    disabled:bool | None = None

class User_DB(User):
    password:str
    refresh_token:str | None = None

