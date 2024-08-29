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
from db.querries.libros import update_register_book
from db.querries.papers import update_register_paper

edit=APIRouter(prefix='/edit')

@edit.get('/')
def root_edit():
    return 'edit Page'

@edit.put('/book/')
async def book_edit(book:Book):
    result=update_register_book(book=book)
    return result

@edit.put('/paper/')
async def book_edit(paper:Paper):
    result=update_register_paper(paper=paper)
    return result