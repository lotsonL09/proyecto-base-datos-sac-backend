from fastapi import APIRouter,HTTPException,status

from entities.book import Book
from entities.equipment import Equipment
from entities.paper import Paper
from entities.proyect import Proyect
from entities.trabajo import Trabajo
from entities.user import User

from db.querries.libros import get_id_title,get_id_author,get_id_persona
from db.querries.libros import get_id_location,get_id_status,insert_book,insert_title_author

create=APIRouter(prefix='/create')

@create.get('/')
async def root():
    return 'Create page'


@create.post('/libro')
async def create_book(book:Book):
    
    #verificamos si el libro existe
    #si no se agrega
    id_title=get_id_title(title=book.title,
                    amount=book.amount)

    #agregar libro
    #Verificar si los autores ya estan en la base de datos
    #Si no, se agrega a la base de datos y se obtiene su id
    id_authors=[]
    for author in book.author:
        author_id=get_id_author(author.name)
        id_authors.append(author_id)

    #ubicacion
    id_location=get_id_location(location=book.location)
    #estado
    id_status=get_id_status(status=book.status)

    #prestado a

    id_persona=get_id_persona(persona=book.borrowed_to)

    #INGRESAR A LA TABLA LIBRO
    id_register_book=insert_book(id_title=id_title,id_location=id_location,
                    id_status=id_status,id_persona=id_persona) #NO PRESTADO
    print('Id del registro en libro',id_register_book)

    for id_author in id_authors:
        print('ids para la db: ',id_title,id_location,id_status,id_author)
        #INGRESAR A LA TABLA titulo autor
        id_register_title_author=insert_title_author(id_title=id_title,
                                                    id_author=id_author)
        print('Id del registro en titulo autor',id_register_title_author)
    return 'Done'

@create.post('/equipo')
async def create_equipment(equipment:Equipment):
    print(equipment.date.strftime("%Y-%m-%d"))
    return 'Done'

@create.post('/paper')
async def create_paper(paper:Paper):
    print(paper.authors)
    return 'Done'

@create.post('/proyecto')
async def create_proyect(proyect:Proyect):
    print(proyect.researches)
    return 'Done'

@create.post('/trabajo')
async def create_trabajo(trabajo:Trabajo):
    print(trabajo)
    return 'Done'

@create.post('/usuario')
async def create_user(user:User):
    print(user)
    return 'Done'