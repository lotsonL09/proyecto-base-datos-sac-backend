from flask import Blueprint,jsonify
from db.db_session import engine
from db.schemas_tables.schemas_tables import libro_table,autor_table,ubicacion_table,estado_table,persona_table,titulo_autor_table,titulo_table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,Select,text


home_bp=Blueprint('home',__name__,url_prefix='/home')

Session=sessionmaker(engine)

func.grouping_sets


@home_bp.route('/')
def root_home():

    query=(Select(
        titulo_table.c.Titulo,
        func.group_concat(
            autor_table.c.Autor,
            '; ', #separator
            autor_table.c.Autor) #order by asc
            .label('autores'),
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

    with Session() as session:
        data=session.execute(query).fetchall()

    print(data[0])

    return 'home page'




