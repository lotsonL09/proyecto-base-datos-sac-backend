from pydantic import BaseModel
# from typing import List

class Email(BaseModel):
    addresses:list[str]


class Password_Reset_Request(BaseModel):
    email:str

class Password_Reset_Confirm(BaseModel):
    new_password:str
    confirm_new_password:str
