from fastapi import HTTPException,status

from sqlalchemy import Select,func
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import (titulo_table,autor_table,ubicacion_table,
                                            estado_table,persona_table,libro_table,
                                            titulo_autor_table,titulo_table,estado_table)

from db.db_session import engine

from entities.book import (Borrowed_to,Book,
                        Author,Book_db,
                        Book_update)

from extra.helper_functions import (execute_insert,execute_delete,
                                    execute_update,get_id,
                                    get_update_query,get_delete_query,
                                    get_insert_query,send_activity_record
                                    )

from entities.user import User

from extra.schemas_function import scheme_book_db

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

querry_get_books=(Select(
        libro_table.c.IdLibro,
        titulo_table.c.Titulo,
        func.aggregate_strings(
            func.concat('(',autor_table.c.IdAutor,',',autor_table.c.Autor,')'),';'
        ).label('autores'),
        func.concat('(',ubicacion_table.c.IdUbi,';',ubicacion_table.c.ubicacion,')'),
        func.concat('(',estado_table.c.IdEstado,';',estado_table.c.estado,')'),
        func.concat(persona_table.c.Nombre,' ',persona_table.c.Apellido).label('nombre_completo'),
        titulo_table.c.Cantidad
    )
    .join(titulo_table        ,titulo_table.c.IdTitulo       ==    libro_table.c.IdTitulo)
    .join(titulo_autor_table  ,titulo_autor_table.c.IdTitulo ==    titulo_table.c.IdTitulo)
    .join(autor_table         ,autor_table.c.IdAutor         ==    titulo_autor_table.c.IdAutor)
    .join(ubicacion_table     ,ubicacion_table.c.IdUbi       ==    libro_table.c.IdUbi)
    .join(estado_table        ,estado_table.c.IdEstado       ==    libro_table.c.IdEstado)
    .join(persona_table       ,persona_table.c.IdPersona     ==    libro_table.c.IdPersona)
    .group_by(
        titulo_table.c.Titulo,
        libro_table.c.IdLibro,
        ubicacion_table.c.ubicacion,
        estado_table.c.estado,
        persona_table.c.Nombre,
        persona_table.c.Apellido)
    )

#QUERRIES

#GET ID functions

def get_book_ids(id:int):
    filters={'IdLibro':id}
    return get_id(table=libro_table,filters=filters)

def get_id_title(title:str,amount):
    filters={'Titulo':title}
    id_title=get_id(table=titulo_table,param='IdTitulo',filters=filters)

    if id_title is None:
        id_title=insert_titulo(title=title,
                            amount=amount)
        return id_title
    else:
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

def get_id_persona(persona:Borrowed_to|None):
    if persona is None: 
        return 1
    filters={'Nombre':persona.first_name,
            'Apellido':persona.last_name}
    id_persona=get_id(table=persona_table,param='IdPersona',filters=filters)

    if id_persona is None:
        id_persona=insert_persona(persona=persona)
        return id_persona
    return id_persona[0]

def insert_author(user:str):
    params={'Autor':user}
    query=get_insert_query(table=autor_table,params=params)
    id=execute_insert(query=query)
    return id

def insert_titulo(title:str,amount:int=1):
    params={'Titulo':title,'Cantidad':amount}
    query=get_insert_query(table=titulo_table,params=params)
    id=execute_insert(query=query)
    return id

def insert_book(id_title:int,id_location:int,
                id_status:int,id_persona:int):
    params={
        'IdTitulo':id_title,
        'IdUbi':id_location,
        'IdPersona':id_persona,
        'IdEstado':id_status
    }
    query=get_insert_query(table=libro_table,params=params)
    id=execute_insert(query=query)
    return id

def insert_persona(persona:Borrowed_to):
    params={'Nombre':persona.first_name,'Apellido':persona.last_name}
    query=get_insert_query(table=persona_table,params=params)
    id=execute_insert(query=query)
    return id

def insert_title_author(id_title:int,id_author:int):
    params={'IdTitulo':id_title,'IdAutor':id_author}
    query=get_insert_query(table=titulo_autor_table,params=params)
    id=execute_insert(query=query)
    return id

def update_title(id_titulo:int,new_title=str):
    query=get_update_query(table=titulo_table,filters={'IdTitulo':id_titulo},params={'Titulo':new_title})
    execute_update(query=query)

def add_author(id_title,author:Author):
    id_author=get_id_author(author=author.name)
    query=get_insert_query(table=titulo_autor_table,params={'IdTitulo':id_title,'IdAutor':id_author})
    return execute_insert(query=query)

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
    id_persona=get_id_persona(persona=borrowed_to)
    query=get_update_query(table=libro_table,filters={'IdLibro':id_book},params={'IdPersona':id_persona})
    execute_update(query=query)
    return id_persona

def update_amount(id_title,amount):
    query=get_update_query(table=titulo_table,filters={'IdTitulo':id_title},params={'Cantidad':amount})
    execute_update(query=query)

def delete_book(id_book:int):
    query=get_delete_query(table=libro_table,params={'IdLibro':id_book})
    execute_delete(query=query)

def delete_title_author(id_title:int):
    query=get_delete_query(table=titulo_autor_table,params={'IdTitulo':id_title})
    execute_delete(query=query)

def delete_title(id_title:int):
    query=get_delete_query(table=titulo_table,params={'IdTitulo':id_title})
    execute_delete(query=query)

def create_register_book(book:Book,user:User):

    id_title=get_id_title(title=book.title,
                    amount=book.amount)

    id_authors=[]
    for author in book.authors:
        author_id=get_id_author(author.name)
        id_authors.append(author_id)

    id_persona=get_id_persona(persona=book.borrowed_to)
    for id_author in id_authors:
        _=insert_title_author(id_title=id_title,
                            id_author=id_author)

    id_book=insert_book(id_title=id_title,id_location=book.location,
                    id_status=book.status,id_persona=id_persona)

    send_activity_record(id_user=user.id,section="books",id_on_section=id_book,action="create")

    return {
        'message':'Libro agregado'
    }

def update_register_book(book:Book_update,user:User):

    result=get_book_ids(book.id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Libro no encontrado")

    book_db=Book_db(**scheme_book_db(result))

    if book.title is not None:
        update_title(id_titulo=book_db.id_title,new_title=book.title)

    authors_added=[]

    if len(book.authors_added) != 0:
        for author in book.authors_added:
            id_author_added=add_author(id_title=book_db.id_title,author=author)
            authors_added.append({
                "id":id_author_added,
                "value":author.name
            })

    if len(book.authors_deleted) != 0:
        for author in book.authors_deleted:
            delete_author(id_title=book_db.id_title,author=author)
    #
    if book.location is not None:
        id_update_location=update_location(id_book=book_db.id_book,id_location=book.location)
    
    if book.status is not None:
        update_status(id_book=book_db.id_book,id_status=book.status)
    #
    
    new_borrowed_to=dict()

    if book.borrowed_to is not None:
        id_update_borrowed_to=update_borrowed_to(id_book=book_db.id_book,borrowed_to=book.borrowed_to)
        new_borrowed_to={
            'id':id_update_borrowed_to,
            'first_name':book.borrowed_to.first_name,
            'last_name':book.borrowed_to.last_name
        }
    else:
        new_borrowed_to=None
    
    if book.amount is not None:
        update_amount(id_title=book_db.id_title,amount=book.amount)
    
    send_activity_record(id_user=user.id,section="books",id_on_section=book.id,action="update")

    return {
        'id':book_db.id_book,
        'authors_added':authors_added,
        'borrowed_to':new_borrowed_to
    }

def delete_register_book(id:int,user:User):
    result=get_book_ids(id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Libro no encontrado")

    book_db=Book_db(**scheme_book_db(result))
    delete_book(id_book=book_db.id_book)
    delete_title_author(id_title=book_db.id_title)
    delete_title(id_title=book_db.id_title)

    send_activity_record(id_user=user.id,section="books",action="delete")

    return {
        "response":'Libro eliminado'
    }
