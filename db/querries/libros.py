from fastapi import HTTPException,status

from sqlalchemy import Select,func,insert,select
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import titulo_table,autor_table,ubicacion_table
from db.schemas_tables.schemas_tables import estado_table,persona_table,libro_table,titulo_autor_table
from db.schemas_tables.schemas_tables import titulo_table,estado_table

from db.db_session import engine

from entities.book import Borrowed_to

from extra.helper_functions import execute_insert,get_id_querry,execute_get

#COMPROBAR

Session=sessionmaker(engine)

querry_get_book_mysql="""
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
        titulo_table.c.Titulo,
        func.aggregate_strings(autor_table.c.Autor,';').label('autores'),
        ubicacion_table.c.ubicacion,
        estado_table.c.estado,
        func.concat(persona_table.c.Nombre,' ',persona_table.c.Apellido).label('nombre_completo')
    )
    .select_from(libro_table)
    .join(titulo_table        ,titulo_table.c.IdTitulo       ==    libro_table.c.IdTitulo)
    .join(titulo_autor_table  ,titulo_autor_table.c.IdTitulo ==    titulo_table.c.IdTitulo)
    .join(autor_table         ,autor_table.c.IdAutor         ==    titulo_autor_table.c.IdAutor)
    .join(ubicacion_table     ,ubicacion_table.c.IdUbi       ==    libro_table.c.IdUbi)
    .join(estado_table        ,estado_table.c.IdEstado       ==    libro_table.c.IdEstado)
    .join(persona_table       ,persona_table.c.IdPersona     ==    libro_table.c.IdPersona)
    .group_by(
        titulo_table.c.Titulo,
        ubicacion_table.c.ubicacion,
        estado_table.c.estado,
        persona_table.c.Nombre,
        persona_table.c.Apellido)
    )

#QUERRIES

querry_get_id_author=get_id_querry(table=autor_table,param=autor_table.c.IdAutor)

querry_get_id_persona=get_id_querry(table=persona_table,param=persona_table.c.IdPersona)

querry_get_id_status=get_id_querry(table=estado_table,param=estado_table.c.IdEstado)

querry_get_id_title=get_id_querry(table=titulo_table,param=titulo_table.c.IdTitulo)

querry_get_id_location=get_id_querry(table=ubicacion_table,param=ubicacion_table.c.IdUbi)


#GET ID functions

def get_id_title(title:str,amount):
    querry=querry_get_id_title.where(titulo_table.c.Titulo == title)

    id_title=execute_get(querry=querry)

    if id_title is None:
        id_title=insert_titulo(title=title,
                                amount=amount)
        return id_title
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail='Este libro ya está registrado')

def get_id_author(author:str):
    querry=querry_get_id_author.where(autor_table.c.Autor == author)

    id_author=execute_get(querry=querry)

    if id_author is None:
        id_author=insert_author(author)
        return id_author
    
    return id_author

def get_id_persona(persona:Borrowed_to|None):
    if persona is None: #TODO: PREGUNTAR A ALVARO SOBRE ESTO
        return 1
    querry=querry_get_id_persona.where((persona_table.c.Nombre == persona.first_name) &
                                    (persona_table.c.Apellido == persona.last_name))
    
    id_persona=execute_get(querry=querry)

    if id_persona is None:
        id_persona=insert_persona(persona=persona)
        return id_persona

    return id_persona

def get_id_location(location):
    querry=querry_get_id_location.where(ubicacion_table.c.ubicacion == location)

    id_location=execute_get(querry=querry)

    return id_location

def get_id_status(status):
    querry=querry_get_id_status.where(estado_table.c.estado == status)

    id_status=execute_get(querry=querry)

    return id_status

#GET QUERRIES INSERT

def get_insert_querry_persona(first_name:str,last_name:str):
    insert_querry=insert(persona_table).values(
        Nombre=first_name,
        Apellido=last_name)
    return insert_querry

def get_insert_querry_title_author(id_title:int,id_author:int):
    insert_querry=insert(titulo_autor_table).values(
        IdTitulo=id_title,
        IdAutor=id_author
    )
    return insert_querry

def get_insert_querry_title(title:str,amount):
    insert_query=insert(titulo_table).values(
        Titulo=title,
        Cantidad=amount
    )
    return insert_query

def get_insert_querry_author(user:str):
    insert_querry=insert(autor_table).values(
        Autor=user
    )
    return insert_querry

def get_insert_querry_book(id_title:int,id_location:int,
                        id_status:int,id_persona:int):
    insert_querry=insert(libro_table).values(
        IdTitulo=id_title,
        IdUbi=id_location,
        IdPersona=id_persona,
        IdEstado=id_status
    )
    return insert_querry

#INSERT REGISTER

def insert_author(user:str):
    querry=get_insert_querry_author(user)
    id=execute_insert(querry=querry)
    return id

def insert_titulo(title:str,amount:int=1):
    querry=get_insert_querry_title(title=title,amount=amount)
    id=execute_insert(querry=querry)
    return id

def insert_book(id_title:int,id_location:int,
                id_status:int,id_persona:int):
    querry=get_insert_querry_book(id_title=id_title,id_location=id_location,
                                id_status=id_status,id_persona=id_persona)
    id=execute_insert(querry=querry)
    return id

def insert_persona(persona:Borrowed_to):
    querry=get_insert_querry_persona(first_name=persona.first_name,
                                    last_name=persona.last_name)
    id=execute_insert(querry=querry)
    return id

def insert_title_author(id_title:str,id_author:id):
    querry=get_insert_querry_title_author(id_title=id_title,
                                        id_author=id_author)
    id=execute_insert(querry=querry)
    return id

