#from flask import Blueprint

from fastapi import APIRouter

from entities.book import Book
from entities.equipment import Equipment
from entities.paper import Paper
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User

from db.querries.libros import update_register_book

update=APIRouter(prefix='/update')

@update.get('/')
def root_update():
    return 'update Page'


@update.post('/libro')
async def edit_book(book:Book):
    result=update_register_book(book=book)
    print(book)
    return 'Done'

@update.post('/equipo')
async def edit_equipment(equipment:Equipment):
    print(equipment.date.strftime("%Y-%m-%d"))
    return 'Done'

@update.post('/paper')
async def edit_paper(paper:Paper):
    print(paper.authors)
    return 'Done'

@update.post('/proyecto')
async def edit_proyect(proyect:Proyect):
    print(proyect.researches)
    return 'Done'

@update.post('/trabajo')
async def edit_trabajo(trabajo:Trabajo):
    print(trabajo)
    return 'Done'

@update.post('/usuario')
async def edit_user(user:User):
    print(user)
    return 'Done'