from pydantic import BaseModel
from datetime import datetime
from entities.user import User_Mongo
from entities.book import Book
from entities.equipment import Equipment
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


class Record_Book(Record):
    previus_version:Book
    new_version:Book

class Record_Equipment(Record):
    previus_version:Equipment
    new_version:Equipment

class Record_Trabajo(Record):
    previus_version:Trabajo
    new_version:Trabajo

class Record_Paper(Record):
    previus_version:Paper
    new_version:Paper

class Record_Project(Record):
    previus_version:Proyect
    new_version:Proyect

class Record_User(Record):
    previus_version:User
    new_version:User