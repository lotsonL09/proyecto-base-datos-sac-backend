from fastapi import status,HTTPException

from sqlalchemy import Select,desc,insert

from db.schemas_tables.schemas_tables import trabajos_table,cursos_table

from entities.trabajo import Trabajo

from extra.helper_functions import get_id_query,execute_get,execute_insert

querry_get_trabajos=(Select(
    trabajos_table.c.idCurso,
    trabajos_table.c.Título,
    cursos_table.c.Curso,
    trabajos_table.c.Año,
    trabajos_table.c.Link)
    .join(cursos_table,cursos_table.c.idCurso  ==  trabajos_table.c.idCurso )
    .filter(trabajos_table.c.Link != 'NOT_FOUND')
    .order_by(trabajos_table.c.Año.asc(),cursos_table.c.Curso.desc()
    )
)

query_get_id_trabajo=get_id_query(table=trabajos_table,param=trabajos_table.c.idTrab)

def get_insert_query_trabajo(trabajo:Trabajo):
    insert_query=insert(trabajos_table).values(
        Título = trabajo.title,
        idCurso = trabajo.course,
        Año = trabajo.year,
        Link = trabajo.link
    )
    return insert_query


def insert_trabajo(trabajo:Trabajo):
    query=get_insert_query_trabajo(trabajo=trabajo)
    id=execute_insert(query=query)
    return id


def get_id_trabajo(trabajo:Trabajo):
    query=query_get_id_trabajo.where(trabajos_table.c.Título == trabajo.title)
    id_trabajo=execute_get(query=query)


    if id_trabajo is None:
        id_trabajo= insert_trabajo(trabajo=trabajo)
        return id_trabajo
    else:
        raise  HTTPException(status_code=status.HTTP_302_FOUND,
                            detail='Este trabajo ya está registrado.')


def create_register_trabajo(trabajo:Trabajo):
    
    _=get_id_trabajo(trabajo=trabajo)

    return 'Registro realizado'

