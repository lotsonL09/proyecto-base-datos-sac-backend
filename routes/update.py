#from flask import Blueprint

from fastapi import APIRouter,Depends
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

from config.auth import auth_user

update=APIRouter(prefix='/update')

@update.get('/')
def root_update():
    return 'update Page'


@update.put('/book')
async def edit_book(book:Book_update,user=Depends(auth_user)):
    result=update_register_book(book=book,user=user)
    return JSONResponse(result)

@update.put('/equipment')
async def edit_equipment(equipment:Equipment,user=Depends(auth_user)):
    result=update_register_equipment(equipment=equipment,user=user)
    return JSONResponse(result)

@update.put('/paper')
async def edit_paper(paper:Paper_update,user=Depends(auth_user)):
    result=update_register_paper(paper=paper,user=user)
    return JSONResponse(result)

@update.put('/project')
async def edit_proyect(project:Proyect_update,user=Depends(auth_user)):
    result=update_register_proyect(project=project,user=user)
    return JSONResponse(result)

@update.put('/trabajo')
async def edit_trabajo(trabajo:Trabajo,user=Depends(auth_user)):
    result=update_register_trabajo(trabajo=trabajo,user=user)
    return JSONResponse(result)

@update.put('/user')
async def edit_user(user=Depends(auth_user)):
    print(user)
    return 'Done'