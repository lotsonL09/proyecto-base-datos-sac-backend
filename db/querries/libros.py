from fastapi import HTTPException,status

from sqlalchemy import Select,func,insert,select,update,delete
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import titulo_table,autor_table,ubicacion_table
from db.schemas_tables.schemas_tables import estado_table,persona_table,libro_table,titulo_autor_table
from db.schemas_tables.schemas_tables import titulo_table,estado_table

from db.db_session import engine

from entities.book import Borrowed_to,Book,Author,Book_db

from extra.helper_functions import execute_insert,get_id_query,execute_get

from extra.schemas_function import scheme_book_db
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
        libro_table.c.IdLibro,
        titulo_table.c.Titulo,
        func.aggregate_strings(autor_table.c.Autor,';').label('autores'),
        ubicacion_table.c.IdUbi,
        estado_table.c.IdEstado,
        func.concat(persona_table.c.Nombre,' ',persona_table.c.Apellido).label('nombre_completo')
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

querry_get_id_author=get_id_query(table=autor_table,param=autor_table.c.IdAutor)

querry_get_id_persona=get_id_query(table=persona_table,param=persona_table.c.IdPersona)

querry_get_id_status=get_id_query(table=estado_table,param=estado_table.c.IdEstado)

querry_get_id_title=get_id_query(table=titulo_table,param=titulo_table.c.IdTitulo)

querry_get_id_location=get_id_query(table=ubicacion_table,param=ubicacion_table.c.IdUbi)


#GET ID functions

def get_book_ids(id:int):
    with Session() as session:
        result = session.execute(libro_table.select()
                                .where(libro_table.c.IdLibro == id)).first()
    return result

def get_id_title(title:str,amount):
    query=querry_get_id_title.where(titulo_table.c.Titulo == title)

    id_title=execute_get(query=query)

    if id_title is None:
        id_title=insert_titulo(title=title,
                                amount=amount)
        return id_title
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail='Este libro ya está registrado')

def get_id_author(author:str):
    query=querry_get_id_author.where(autor_table.c.Autor == author)

    id_author=execute_get(query=query)

    if id_author is None:
        id_author=insert_author(author)
        return id_author
    else:
        return id_author[0]

def get_id_persona(persona:Borrowed_to|None):
    if persona is None: #TODO: PREGUNTAR A ALVARO SOBRE ESTO
        return 1
    querry=querry_get_id_persona.where((persona_table.c.Nombre == persona.first_name) &
                                    (persona_table.c.Apellido == persona.last_name))
    
    id_persona=execute_get(querry=querry)[0]
    
    if id_persona is None:
        id_persona=insert_persona(persona=persona)
        return id_persona
    return id_persona

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
    query=get_insert_querry_author(user)
    id=execute_insert(query=query)
    return id

def insert_titulo(title:str,amount:int=1):
    query=get_insert_querry_title(title=title,amount=amount)
    id=execute_insert(query=query)
    return id

def insert_book(id_title:int,id_location:int,
                id_status:int,id_persona:int):
    query=get_insert_querry_book(id_title=id_title,id_location=id_location,
                                id_status=id_status,id_persona=id_persona)
    id=execute_insert(query=query)
    return id

def insert_persona(persona:Borrowed_to):
    query=get_insert_querry_persona(first_name=persona.first_name,
                                    last_name=persona.last_name)
    id=execute_insert(query=query)
    return id

def insert_title_author(id_title:int,id_author:int):
    query=get_insert_querry_title_author(id_title=id_title,
                                        id_author=id_author)
    id=execute_insert(query=query)
    return id

#UPDATE TITULO

def update_title(id_titulo:int,new_title=str):
    update_querry=(update(titulo_table)
                .where(titulo_table.c.IdTitulo == id_titulo)
                .values(Titulo=new_title))

    with Session() as session:
        session.execute(update_querry)
        session.commit()

def get_querry_delete_title_autor(id_title:int,id_author:int):
    return delete(titulo_autor_table).where(
        titulo_autor_table.c.IdTitulo == id_title,
        titulo_autor_table.c.IdAutor == id_author
    )

def update_author(id_tittle,authors:list[Author]):
    
    with Session() as session:
        results=session.execute(titulo_autor_table.select().where(titulo_autor_table.c.IdTitulo == id_tittle)).fetchall()

        for register in results:
            id_old_author=register[1]
            querry=get_querry_delete_title_autor(id_title=id_tittle,id_author=id_old_author)
            session.execute(querry)
            session.commit()

        for author in authors:
            id_author=get_id_author(author=author.name)

            id=insert_title_author(id_title=id_tittle,id_author=id_author)

def update_location(id_book,id_location:str):
    #id_location=get_id_location(location=location)
    update_querry=(update(libro_table)
                .where(libro_table.c.IdLibro == id_book)
                .values(IdUbi=id_location))
    
    with Session() as session:
        session.execute(update_querry)
        session.commit()

def update_status(id_book,id_status:str):
    #id_status=get_id_status(status=status)
    update_querry=(update(libro_table)
                .where(libro_table.c.IdLibro == id_book)
                .values(IdEstado=id_status))
    
    with Session() as session:
        session.execute(update_querry)
        session.commit()

def update_borrowed_to(id_book,borrowed_to:Borrowed_to):
    id_persona=get_id_persona(persona=borrowed_to)
    update_querry=(update(libro_table)
                .where(libro_table.c.IdLibro == id_book)
                .values(IdPersona=id_persona))
    with Session() as session:
        session.execute(update_querry)
        session.commit()

def update_amount(id_title,amount):
    update_querry=(update(titulo_table)
                .where(titulo_table.c.IdTitulo == id_title)
                .values(Cantidad=amount))
    with Session() as session:
        session.execute(update_querry)
        session.commit()


#DELETE LIBRO

def get_querry_delete_book(id_book:str):
    return delete(libro_table).where(
        libro_table.c.IdLibro == id_book
    )

def get_querry_delete_title_author(id_title:str):
    return delete(titulo_autor_table).where(
        titulo_autor_table.c.IdTitulo == id_title
    )

def get_querry_delete_title(id_title:str):
    return delete(titulo_table).where(
        titulo_table.c.IdTitulo == id_title
    )

def delete_book(id_book:str):
    querry=get_querry_delete_book(id_book=id_book)
    with Session() as session:
        session.execute(querry)
        session.commit()

def delete_title_author(id_title:str):
    querry=get_querry_delete_title_author(id_title=id_title)
    with Session() as session:
        session.execute(querry)
        session.commit()

def delete_title(id_title:str):
    querry=get_querry_delete_title(id_title=id_title)
    with Session() as session:
        session.execute(querry)
        session.commit()

#DELETE TITULO


#FUNCTIONS

def create_register_book(book:Book):

    id_title=get_id_title(title=book.title,
                    amount=book.amount)

    id_authors=[]
    for author in book.author:
        author_id=get_id_author(author.name)
        id_authors.append(author_id)

    id_persona=get_id_persona(persona=book.borrowed_to)
    for id_author in id_authors:
        _=insert_title_author(id_title=id_title,
                            id_author=id_author)

    _=insert_book(id_title=id_title,id_location=book.location,
                    id_status=book.status,id_persona=id_persona)

    return 'Registro realizado'

def update_register_book(book:Book):

    result=get_book_ids(book.id)
    book_db=Book_db(**scheme_book_db(result))
    #print('IDS',book_db)

    if book.title is not None:
        update_title(id_titulo=book_db.id_title,new_title=book.title)
    if len(book.author) != 0:
        update_author(id_tittle=book_db.id_title,authors=book.author)
    #
    if book.location is not None:
        update_location(id_book=book_db.id_book,id_location=book.location)
    #
    if book.status is not None:
        update_status(id_book=book_db.id_book,id_status=book.status)
    #
    if book.borrowed_to is not None:
        update_borrowed_to(id_book=book_db.id_book,borrowed_to=book.borrowed_to)
    if book.amount is not None:
        update_amount(id_title=book_db.id_title,amount=book.amount)
    
    return 'Libro actualizado'


def delete_register_book(id:int):
    result=get_book_ids(id)
    book_db=Book_db(**scheme_book_db(result))
    delete_book(id_book=book_db.id_book)
    delete_title_author(id_title=book_db.id_title)
    delete_title(id_title=book_db.id_title)
    return 'Libro eliminado'
