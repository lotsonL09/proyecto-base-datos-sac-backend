#from flask import Blueprint

from fastapi import APIRouter

from entities.book import Book
from entities.equipment import Equipment
from entities.paper import Paper
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User

edit=APIRouter(prefix='/edit')

@edit.get('/')
def root_edit():
    return 'edit Page'

@edit.post('/libro')
async def edit_book(book:Book):
    print(book)
    return 'Done'

@edit.post('/equipo')
async def edit_equipment(equipment:Equipment):
    print(equipment.date.strftime("%Y-%m-%d"))
    return 'Done'

@edit.post('/paper')
async def edit_paper(paper:Paper):
    print(paper.authors)
    return 'Done'

@edit.post('/proyecto')
async def edit_proyect(proyect:Proyect):
    print(proyect.researches)
    return 'Done'

@edit.post('/trabajo')
async def edit_trabajo(trabajo:Trabajo):
    print(trabajo)
    return 'Done'

@edit.post('/usuario')
async def edit_user(user:User):
    print(user)
    return 'Done'