from pydantic import BaseModel

class Role(BaseModel):
    id:int | None = None
    value:str | None = None

class User_Mongo(BaseModel):
    id:int|None = None
    user_name:str | None = None

class Role(BaseModel):
    id:int
    value:str

class User(BaseModel):
    id: int |None =None
    user_name:str | None = None
    first_name:str | None = None
    last_name:str | None = None
    email:str | None = None
    role:Role | None = None 
    phone:str | None = None
    disabled:bool | None = None

class User_DB(User):
    password:str
    refresh_token:str | None = None

