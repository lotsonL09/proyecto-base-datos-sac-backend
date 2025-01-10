from fastapi import status,HTTPException

from sqlalchemy import Select,insert,update,delete

from db.schemas_tables.schemas_tables import trabajos_table,cursos_table

from entities.trabajo import Trabajo

from db.querries.records import create_record

from extra.helper_functions import (get_id_query,execute_get,
                                    execute_insert,execute_update,
                                    execute_delete,send_activity_record,
                                    get_data)

from entities.user import User

query_get_trabajos=(Select(
    trabajos_table.c.idTrab,
    trabajos_table.c.Título,
    cursos_table.c.idCurso,
    cursos_table.c.Curso,
    trabajos_table.c.Año,
    trabajos_table.c.Link)
    .join(cursos_table,cursos_table.c.idCurso  ==  trabajos_table.c.idCurso )
    .filter(trabajos_table.c.Link != 'NOT_FOUND')
    .order_by(trabajos_table.c.Año.asc(),cursos_table.c.Curso.desc()
    )
)

query_get_id_trabajo=get_id_query(table=trabajos_table,param=trabajos_table.c.idTrab)

def get_trabajo(id):
    query=query_get_trabajos.where(trabajos_table.c.idTrab == id)
    json_data=get_data(section='trabajos',query=query)
    try:
        return Trabajo(**json_data[0])
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Paper not found in database')

def get_insert_query_trabajo(trabajo:Trabajo):
    insert_query=insert(trabajos_table).values(
        Título = trabajo.title,
        idCurso = trabajo.course.id,
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

def create_register_trabajo(trabajo:Trabajo,user:User):
    
    trabajo.id=get_id_trabajo(trabajo=trabajo)

    create_record(id_user=user.id,username=user.user_name,section="trabajo",action='create',new_data=trabajo)

    return {
        "response":'Trabajo agregado'
    }

def update_title(id_trabajo:int,title:str):
    update_query=(update(trabajos_table)
                .where(trabajos_table.c.idTrab == id_trabajo)
                .values(Título = title))
    
    execute_update(query=update_query)

def update_course(id_trabajo:int,id_course:int):
    update_query=(update(trabajos_table)
                .where(trabajos_table.c.idTrab == id_trabajo)
                .values(idCurso = id_course))
    
    execute_update(query=update_query)

def update_year(id_trabajo:int,year:str):
    update_query=(update(trabajos_table)
                .where(trabajos_table.c.idTrab == id_trabajo)
                .values(Año = year))
    
    execute_update(query=update_query)

def update_link(id_trabajo:int,link:str):
    update_query=(update(trabajos_table)
                .where(trabajos_table.c.idTrab == id_trabajo)
                .values(Link = link))
    
    execute_update(query=update_query)

def update_register_trabajo(trabajo:Trabajo,user:User):

    previous_data=get_trabajo(id=trabajo.id)

    if trabajo.title is not None:
        update_title(id_trabajo=trabajo.id,title=trabajo.title)
    if trabajo.course is not None:
        update_course(id_trabajo=trabajo.id,id_course=trabajo.course.id)
    if trabajo.year is not None:
        update_year(id_trabajo=trabajo.id,year=trabajo.year)
    if trabajo.link is not None:
        update_link(id_trabajo=trabajo.id,link=trabajo.link)
    
    create_record(id_user=user.id,username=user.user_name,section="trabajo",action='update',new_data=trabajo,previous_data=previous_data)

    return {
        "response":"Trabajo actualizado"
    }

def delete_trabajo(id_trabajo:int):
    delete_query=(delete(trabajos_table).where(
        trabajos_table.c.idTrab == id_trabajo,
    ))
    execute_delete(query=delete_query)

def delete_register_trabajo(id_trabajo:int,user:User):
    previous_data=get_trabajo(id=id_trabajo)
    delete_trabajo(id_trabajo=id_trabajo)
    create_record(id_user=user.id,username=user.user_name,section="paper",action='delete',previous_data=previous_data)
    return {
        "response":'Trabajo eliminado'
    }
