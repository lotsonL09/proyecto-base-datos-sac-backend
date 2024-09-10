#from flask import Blueprint

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from entities.book import Book_update
from entities.equipment import Equipment
from entities.paper import Paper_update
from entities.proyect import Proyect_update
from entities.trabajo import Trabajo
from entities.user import User

from db.querries.libros import update_register_book
from db.querries.papers import update_register_paper
from db.querries.proyectos import update_register_proyect
from db.querries.trabajos import update_register_trabajo
from db.querries.equipos import update_register_equipment

update=APIRouter(prefix='/update')

@update.get('/')
def root_update():
    return 'update Page'


@update.put('/book')
async def edit_book(book:Book_update):
    result=update_register_book(book=book)
    return JSONResponse(result)

@update.put('/equipment')
async def edit_equipment(equipment:Equipment):
    result=update_register_equipment(equipment=equipment)
    return JSONResponse(result)

@update.put('/paper')
async def edit_paper(paper:Paper_update):
    result=update_register_paper(paper=paper)
    return JSONResponse(result)

@update.put('/project')
async def edit_proyect(proyect:Proyect_update):
    result=update_register_proyect(proyect=proyect)
    return JSONResponse(result)

@update.put('/trabajo')
async def edit_trabajo(trabajo:Trabajo):
    result=update_register_trabajo(trabajo=trabajo)
    return JSONResponse(result)

@update.put('/user')
async def edit_user(user:User):
    print(user)
    return 'Done'