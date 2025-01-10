#from flask import Blueprint

from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from db.querries.libros import delete_register_book
from db.querries.papers import delete_register_paper
from db.querries.proyectos import delete_register_proyect
from db.querries.trabajos import delete_register_trabajo
from db.querries.equipos import delete_register_equipment
from db.querries.users import delete_register_user

from config.auth import auth_user

delete=APIRouter(prefix='/delete')

@delete.get('/')
def root_delete():
    return 'delete Page'

@delete.delete('/book/{id}')
async def book_delete(id:int,user=Depends(auth_user)):
    result=delete_register_book(id=id,user=user)
    return JSONResponse(result)

@delete.delete('/paper/{id}')
async def book_delete(id:int,user=Depends(auth_user)):
    result=delete_register_paper(id_paper=id,user=user)
    return JSONResponse(result)

@delete.delete('/project/{id}')
async def book_proyect(id:int,user=Depends(auth_user)):
    result=delete_register_proyect(id_proyect=id,user=user)
    return JSONResponse(result)

@delete.delete('/trabajo/{id}')
async def book_proyect(id:int,user=Depends(auth_user)):
    result=delete_register_trabajo(id_trabajo=id,user=user)
    return JSONResponse(result)


@delete.delete('/equipment/{id}')
async def book_proyect(id:int,user=Depends(auth_user)):
    result=delete_register_equipment(id_equipment=id,user=user)
    return JSONResponse(result)

@delete.delete('/user/{id}')
async def book_proyect(id:int,user=Depends(auth_user)):
    result=delete_register_user(id_user=id,user=user)
    return JSONResponse(result)