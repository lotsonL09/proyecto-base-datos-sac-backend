from pydantic import BaseModel

class Category(BaseModel):
    id:int | None = None
    value:str | None = None

class User(BaseModel):
    id: int |None =None
    user_name:str | None = None
    first_name:str | None = None
    last_name:str | None = None
    email:str | None = None
    id_category:int | None = None #id of category
    phone:str | None = None
    disabled:bool | None = None

class User_DB(User):
    password:str
    refresh_token:str | None = None

