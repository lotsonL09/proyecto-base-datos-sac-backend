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
