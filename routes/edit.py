#from flask import Blueprint

from fastapi import APIRouter

from entities.book import Book
from entities.equipment import Equipment
from entities.paper import Paper
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User
from entities.book import Book

from entities.book import Book_db
from db.querries.libros import get_book_ids,update_title,update_author,update_location,update_status,update_borrowed_to,update_amount
from extra.schemas_function import scheme_book_db
edit=APIRouter(prefix='/edit')

@edit.get('/')
def root_edit():
    return 'edit Page'

@edit.put('/book/')
async def book_edit(book:Book):
    
    result=get_book_ids(book.id)
    book_db=Book_db(**scheme_book_db(result))

    # print(book_db.id_book)
    # print(book_db.id_location)
    # print(book_db.id_persona)
    # print(book_db.id_status)
    # print(book_db.id_title)

    if book.title is not None:
        update_title(id_titulo=book_db.id_title,new_title=book.title)
    if len(book.author) != 0:
        update_author(id_tittle=book_db.id_title,authors=book.author)
    #
    if book.location is not None:
        update_location(id_book=book_db.id_book,location=book.location)
    #
    if book.status is not None:
        update_status(id_book=book_db.id_book,status=book.status)
    #
    if book.borrowed_to is not None:
        update_borrowed_to(id_book=book_db.id_book,borrowed_to=book.borrowed_to)
    if book.amount is not None:
        update_amount(id_title=book_db.id_title,amount=book.amount)
    
    return 'Done'