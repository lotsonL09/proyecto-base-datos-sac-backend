from fastapi import APIRouter,Depends

from entities.book import Book
from entities.equipment import Equipment
from entities.paper import Paper
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User

from db.querries.libros import create_register_book
from db.querries.papers import create_register_paper
from db.querries.proyectos import create_register_proyect
from db.querries.trabajos import create_register_trabajo
from db.querries.equipos import create_register_equipment

from config.auth import auth_user

create=APIRouter(prefix='/create')

@create.get('/')
async def root():
    return 'Create page'


@create.post('/book')
async def create_book(book:Book,user=Depends(auth_user)):
    result=create_register_book(book=book,user=user)
    return result

@create.post('/equipment')
async def create_equipment(equipment:Equipment,user=Depends(auth_user)):
    result=create_register_equipment(equipment=equipment,user=user)
    return result

@create.post('/paper')
async def create_paper(paper:Paper,user=Depends(auth_user)):
    result=create_register_paper(paper=paper,user=user)
    return result

@create.post('/project')
async def create_proyect(proyect:Proyect,user=Depends(auth_user)):
    result=create_register_proyect(proyect=proyect,user=user)
    return result

@create.post('/trabajo')
async def create_trabajo(trabajo:Trabajo,user=Depends(auth_user)):
    result=create_register_trabajo(trabajo=trabajo,user=user)
    return result

@create.post('/user')
async def create_user(user=Depends(auth_user)):
    print(user)
    return 'Done'