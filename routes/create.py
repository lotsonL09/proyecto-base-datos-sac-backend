from fastapi import APIRouter

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

create=APIRouter(prefix='/create')

@create.get('/')
async def root():
    return 'Create page'


@create.post('/book')
async def create_book(book:Book):
    result=create_register_book(book=book)
    return result

@create.post('/equipment')
async def create_equipment(equipment:Equipment):
    result=create_register_equipment(equipment=equipment)
    return result

@create.post('/paper')
async def create_paper(paper:Paper):
    result=create_register_paper(paper=paper)
    return result

@create.post('/project')
async def create_proyect(proyect:Proyect):
    result=create_register_proyect(proyect=proyect)
    return result

@create.post('/trabajo')
async def create_trabajo(trabajo:Trabajo):
    result=create_register_trabajo(trabajo=trabajo)
    return result

@create.post('/user')
async def create_user(user:User):
    print(user)
    return 'Done'