#from flask import Blueprint

from fastapi import APIRouter

from db.querries.libros import delete_register_book
from db.querries.papers import delete_register_paper

from extra.schemas_function import scheme_book_db

delete=APIRouter(prefix='/delete')

@delete.get('/')
def root_delete():
    return 'delete Page'

@delete.delete('/book/{id}')
async def book_delete(id:str):
    result=delete_register_book(id=id)
    return result


@delete.delete('/paper/{id}')
async def book_delete(id:str):
    result=delete_register_paper(id_paper=id)
    return result