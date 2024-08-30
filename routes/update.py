#from flask import Blueprint

from fastapi import APIRouter

from entities.book import Book
from entities.equipment import Equipment
from entities.paper import Paper_update
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User

from db.querries.libros import update_register_book
from db.querries.papers import update_register_paper

update=APIRouter(prefix='/update')

@update.get('/')
def root_update():
    return 'update Page'


@update.put('/libro')
async def edit_book(book:Book):
    result=update_register_book(book=book)
    return result

@update.put('/equipo')
async def edit_equipment(equipment:Equipment):
    print(equipment.date.strftime("%Y-%m-%d"))
    return 'Done'

@update.put('/paper')
async def edit_paper(paper:Paper_update):
    result=update_register_paper(paper=paper)
    return result

@update.put('/proyecto')
async def edit_proyect(proyect:Proyect):
    print(proyect.researches)
    return 'Done'

@update.put('/trabajo')
async def edit_trabajo(trabajo:Trabajo):
    print(trabajo)
    return 'Done'

@update.put('/usuario')
async def edit_user(user:User):
    print(user)
    return 'Done'