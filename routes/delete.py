#from flask import Blueprint

from fastapi import APIRouter

from db.querries.libros import delete_register_book
from db.querries.papers import delete_register_paper
from db.querries.proyectos import delete_register_proyect
from db.querries.trabajos import delete_register_trabajo

delete=APIRouter(prefix='/delete')

@delete.get('/')
def root_delete():
    return 'delete Page'

@delete.delete('/book/{id}')
async def book_delete(id:int):
    result=delete_register_book(id=id)
    return result

@delete.delete('/paper/{id}')
async def book_delete(id:int):
    result=delete_register_paper(id_paper=id)
    return result

@delete.delete('/proyect/{id}')
async def book_proyect(id:int):
    result=delete_register_proyect(id_proyect=id)
    return result

@delete.delete('/trabajo/{id}')
async def book_proyect(id:int):
    result=delete_register_trabajo(id_trabajo=id)
    return result