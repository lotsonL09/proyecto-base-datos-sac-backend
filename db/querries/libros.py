from fastapi import HTTPException,status

from sqlalchemy import Select,func,select
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import (autor_table,ubicacion_table,
                                            estado_table,libro_table,usuario_table,
                                            libro_autor_table,estado_table,
                                            roles_table,libro_usuario_table)

from db.mysql_session.db_session import engine

from entities.book import (Borrowed_to,
                        Book_Create,
                        Author,Book_db,
                        Book_update)

from extra.helper_functions import (execute_insert,execute_delete,
                                    execute_update,get_id,
                                    get_update_query,get_delete_query,
                                    get_insert_query,
                                    execute_get,get_data,execute_get_all
                                    )

from entities.user import User

from extra.schemas_function import scheme_book_db

from db.querries.records import create_record

from db.querries.estados import get_status_book_equipment

from db.querries.ubicacion import get_location

Session=sessionmaker(engine)

"""
SELECT
        libro.IdLibro,
        titulo.Titulo,
        GROUP_CONCAT(autor.Autor ORDER BY autor.Autor ASC SEPARATOR '; ') AS autores,
        ubicación.ubicacion,
        estado.estado,
        CONCAT(persona.nombre, ' ', persona.apellido) AS nombre_completo
    FROM libro
    INNER JOIN titulo ON titulo.IdTitulo = libro.IdTitulo
    INNER JOIN titulo_autor ON titulo_autor.IdTitulo = titulo.IdTitulo
    INNER JOIN autor ON autor.IdAutor = titulo_autor.IdAutor
    INNER JOIN ubicación ON ubicación.IdUbi = libro.IdUbi
    INNER JOIN estado ON estado.IdEstado = libro.IdEstado
    INNER JOIN persona ON persona.IdPersona = libro.IdPersona
    GROUP BY libro.IdLibro, titulo.Titulo, ubicación.ubicacion, estado.estado, persona.nombre, persona.apellido
"""

# func.group_concat(
#             autor_table.c.Autor,
#             ';' #separator
#             ).label('autores'),

query_get_books=(Select(
        libro_table.c.IdLibro,
        libro_table.c.Titulo,
        func.aggregate_strings(
            func.concat('(',autor_table.c.IdAutor,',',autor_table.c.Autor,')'),';'
        ),
        func.concat('(',ubicacion_table.c.IdUbi,';',ubicacion_table.c.ubicacion,')'),
        func.concat('(',estado_table.c.IdEstado,';',estado_table.c.estado,')'),
        libro_table.c.Cantidad
    )
    .select_from(libro_table)
    .join(libro_autor_table   ,libro_table.c.IdLibro         ==    libro_autor_table.c.IdLibro)
    .join(autor_table         ,autor_table.c.IdAutor         ==    libro_autor_table.c.IdAutor)
    .join(ubicacion_table     ,ubicacion_table.c.IdUbi       ==    libro_table.c.IdUbi)
    .join(estado_table        ,estado_table.c.IdEstado       ==    libro_table.c.IdEstado)
    .group_by(
        libro_table.c.Titulo,
        libro_table.c.IdLibro,
        ubicacion_table.c.ubicacion,
        estado_table.c.estado)
    )

query_get_borrowed_to=(Select(
    libro_usuario_table.c.IdUsuario,
    usuario_table.c.user_name,
    roles_table.c.id,
    roles_table.c.name)
    .join(libro_usuario_table , libro_usuario_table.c.IdUsuario == usuario_table.c.id_usuario)
    .join(roles_table       ,usuario_table.c.id_role    == roles_table.c.id))
#QUERRIES

#GET ID functions

def get_book(id) -> Book_Create:
    query=query_get_books.where(libro_table.c.IdLibro==id)
    json_data=get_data(section='books',query=query)[0]
    if json_data:
        return Book_Create(**json_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Book not found in database')

def get_book_ids(id:int):
    filters={'IdLibro':id}
    return get_id(table=libro_table,filters=filters)

def get_borrowed_to(id_libro:int):
    users=[]
    query=query_get_borrowed_to.where(libro_usuario_table.c.IdLibro == id_libro)
    result=execute_get_all(query=query)
    if len(result) == 0:
        return 'No prestado'
    else:
        for user in result:
            users.append({
                'id':user[0],
                'user_name':user[1],
                'role':{
                    'id':user[2],
                    'value':user[3]
                }
            })
        return users


def get_title(title:str,amount):
    filters={'Titulo':title}
    id_title=get_id(table=libro_table,param='Titulo',filters=filters)

    if id_title is not None:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail='Este libro ya está registrado')

def get_id_author(author:str):

    filters={'Autor':author}

    id_author=get_id(table=autor_table,param='IdAutor',filters=filters)

    if id_author is None:
        id_author=insert_author(author)
        return id_author
    else:
        return id_author[0]

def get_id_user(user:Borrowed_to|None):
    if user is None: 
        return None
    else:
        filters={'id':user.id}
        id_user=get_id(table=usuario_table,param='id_usuario',filters=filters)
        if id_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User not found in database')
        return id_user

def insert_author(user:str):
    params={'Autor':user}
    query=get_insert_query(table=autor_table,params=params)
    id=execute_insert(query=query)
    return id

# def insert_titulo(title:str,amount:int=1):
#     params={'Titulo':title,'Cantidad':amount}
#     query=get_insert_query(table=titulo_table,params=params)
#     id=execute_insert(query=query)
#     return id

def insert_book(title:str,id_location:int,
                id_status:int,amount:int):
    params={
        'Titulo':title,
        'IdUbi':id_location,
        'IdEstado':id_status,
        'Cantidad':amount
    }
    query=get_insert_query(table=libro_table,params=params)
    id=execute_insert(query=query)
    return id

def insert_persona(persona:Borrowed_to):
    params={'Nombre':persona.first_name,'Apellido':persona.last_name}
    query=get_insert_query(table=persona_table,params=params)
    id=execute_insert(query=query)
    return id

def insert_book_author(id_book:int,id_author:int):
    params={'IdLibro':id_book,'IdAutor':id_author}
    query=get_insert_query(table=libro_autor_table,params=params)
    id=execute_insert(query=query)
    return id

def update_title(id_libro:int,new_title=str):
    query=get_update_query(table=libro_table,filters={'IdLibro':id_libro},params={'Titulo':new_title})
    execute_update(query=query)

def add_author(id_title,author:Author):
    id_author=get_id_author(author=author.value)
    query=get_insert_query(table=titulo_autor_table,params={'IdTitulo':id_title,'IdAutor':id_author})
    execute_insert(query=query)
    return id_author

def delete_author(id_title,author:Author):
    query=get_delete_query(table=titulo_autor_table,params={'IdTitulo':id_title,'IdAutor':author.id})
    _=execute_delete(query=query)

def update_location(id_book,id_location:str):
    query=get_update_query(table=libro_table,filters={'IdLibro':id_book},params={'IdUbi':id_location})
    execute_update(query=query)

def update_status(id_book,id_status:str):
    query=get_update_query(table=libro_table,filters={'IdLibro':id_book},params={'IdEstado':id_status})
    execute_update(query=query)

def update_borrowed_to(id_book,borrowed_to:Borrowed_to):
    query=get_update_query(table=libro_usuario_table,filters={'IdLibro':id_book},params={'IdUsuario':borrowed_to.id})
    execute_update(query=query)

def add_borrowed_to(id_book,borrowed_to:Borrowed_to):
    query=get_insert_query(table=libro_usuario_table,params={'IdUsuario':borrowed_to.id,"IdLibro":id_book})
    execute_insert(query=query)

def delete_borrowed_to(borrowed_to:Borrowed_to):
    query=get_delete_query(table=libro_usuario_table,params={'IdUsuario':borrowed_to.id})
    execute_delete(query=query)

def update_amount(id_libro,amount):
    query=get_update_query(table=libro_table,filters={'IdLibro':id_libro},params={'Cantidad':amount})
    execute_update(query=query)

def delete_book(id_book:int):
    query=get_delete_query(table=libro_table,params={'IdLibro':id_book})
    execute_delete(query=query)

def delete_libro_author(id_book:int):
    query=get_delete_query(table=libro_autor_table,params={'IdLibro':id_book})
    execute_delete(query=query)

def delete_libro_usuario(id_book:int):
    query=get_delete_query(table=libro_usuario_table,params={'IdLibro':id_book})
    execute_delete(query=query)

def delete_title(id_title:int):
    query=get_delete_query(table=titulo_table,params={'IdTitulo':id_title})
    execute_delete(query=query)

def create_register_book(book:Book_Create,user:User):

    get_title(title=book.title,amount=book.amount)

    id_book=insert_book(title=book.title,id_location=book.location.id,
                    id_status=book.status.id,amount=book.amount)
    
    book.id=id_book

    for author in book.authors:
        if author.id is None:
            author_id=get_id_author(author.value)
            author.id=author_id
        _=insert_book_author(id_book=book.id,id_author=author.id)

    if len(book.borrowed_to) != 0:
        for user_borrowed in book.borrowed_to:
            add_borrowed_to(id_book=book.id,borrowed_to=user_borrowed)

    create_record(id_user=user.id,username=user.user_name,section="book",action='create',new_data=book)

    return {
        'message':'Libro agregado'
    }

def update_register_book(book:Book_update,user:User):

    previous_data=get_book(id=book.id)

    if previous_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Libro no encontrado")

    if book.title is not None:
        update_title(id_libro=book.id,new_title=book.title)

    if len(book.authors_added) != 0:
        for author in book.authors_added:
            id_author_added=add_author(id_title=book.title.id,author=author)
            if author.id is None:
                author.id=id_author_added

    if len(book.authors_deleted) != 0:
        for author in book.authors_deleted:
            delete_author(id_title=book.title.id,author=author)

    if book.location is not None:
        update_location(id_book=book.id,id_location=book.location.id)

    if book.status is not None:
        update_status(id_book=book.id,id_status=book.status.id)

    if len(book.borrowed_to_added) != 0:
        for user_borrowed in book.borrowed_to_added:
            add_borrowed_to(id_book=book.id,borrowed_to=user_borrowed)

    if len(book.borrowed_to_deleted) != 0:
        for user_borrowed in book.borrowed_to_deleted:
            delete_borrowed_to(borrowed_to=user_borrowed)

    if book.amount is not None:
        update_amount(id_libro=book.id,amount=book.amount)

    create_record(id_user=user.id,username=user.user_name,section="book",action='update',new_data=book,previous_data=previous_data)
    
    return {
        "response":'Libro updated'
    }


def delete_register_book(id:int,user:User):
    result=get_book_ids(id)

    previous_data=get_book(id=id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Libro no encontrado")

    book_db=Book_db(**scheme_book_db(result))
    delete_libro_author(id_book=book_db.id_book)
    delete_libro_usuario(id_book=book_db.id_book)
    delete_book(id_book=book_db.id_book)

    create_record(id_user=user.id,username=user.user_name,section="book",action='delete',previous_data=previous_data)

    return {
        "response":'Libro eliminado'
    }
