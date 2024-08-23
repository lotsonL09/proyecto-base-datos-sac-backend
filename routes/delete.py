#from flask import Blueprint

from fastapi import APIRouter

from entities.book import Book_db

from db.querries.libros import delete_book,delete_title,delete_title_author,Book,get_book_ids

from extra.schemas_function import scheme_book_db

delete=APIRouter(prefix='/delete')

@delete.get('/')
def root_delete():
    return 'delete Page'

@delete.put('/book/{id}')
async def book_delete(id:str):
    result=get_book_ids(id)
    book_db=Book_db(**scheme_book_db(result))
    
    print(book_db)

    return 'Book deleted'