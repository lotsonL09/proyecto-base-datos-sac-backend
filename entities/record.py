from pydantic import BaseModel
from datetime import datetime
from entities.user import User_Mongo
from entities.book import Book_Create
from entities.equipment import Equipment_Create
from entities.trabajo import Trabajo
from entities.paper import Paper
from entities.proyect import Proyect
from entities.user import User

# class Record(BaseModel):
#     user_name:str
#     message:str
#     table:str
#     time: datetime


class Record(BaseModel):
    user:User_Mongo
    time:datetime
    section:str
    action:str

