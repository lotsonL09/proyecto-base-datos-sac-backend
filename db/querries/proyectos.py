from fastapi import status,HTTPException

from sqlalchemy import Select,func,distinct,insert,delete

from db.schemas_tables.schemas_tables import (proyec_invest_table,proyectos_table,
                                            convenios_table,miembros_table,
                                            proyec_conv_table,estatus_table,
                                            cargos_table)

from extra.helper_functions import (execute_insert,execute_update,
                                    execute_delete,get_id,
                                    get_insert_query,get_update_query,
                                    get_delete_query,send_activity_record,
                                    get_data)

from entities.user import User

from extra.schemas_function import scheme_proyect_to_db

from entities.proyect import Proyect,Proyect_db,Agreement,Proyect_update,Period

from entities.share.shared import Member

from db.querries.records import create_record

coordinador=miembros_table.alias('coordinador')
investigador=miembros_table.alias('investigador')

cargos_coordinador = cargos_table.alias('cargos_coordinador')
cargos_investigador = cargos_table.alias('cargos_investigador')

query_get_proyectos=(Select(
    proyectos_table.c.idProyec,
    proyectos_table.c.Proyecto,
    func.concat(coordinador.c.idMiembro,';',coordinador.c.nombre,';',coordinador.c.apellido,';',cargos_coordinador.c.idCargo,';',cargos_coordinador.c.cargo).label('Coordinador'),
    func.aggregate_strings(
        distinct(func.concat('(',investigador.c.idMiembro,',',investigador.c.nombre,',',investigador.c.apellido,',',cargos_investigador.c.idCargo,',',cargos_investigador.c.cargo,')'))
            .op('ORDER BY')(func.concat('(',investigador.c.idMiembro,',',investigador.c.nombre,',',investigador.c.apellido,')')),
        ';'
    ).label('Investigadores'),
    func.aggregate_strings(
        distinct(convenios_table.c.Convenio)
            .op('ORDER BY')(convenios_table.c.Convenio),
        ';'
    ).label('Convenios'),
    func.concat('(',estatus_table.c.idEstatus,';',estatus_table.c.Estatus,')'),
    func.concat(proyectos_table.c.Año_in,';',proyectos_table.c.Año_fin)
)
.join(proyec_invest_table   ,   proyec_invest_table.c.Proyec_idP ==   proyectos_table.c.idProyec)
.join(investigador          ,   investigador.c.idMiembro         ==   proyec_invest_table.c.idMiembro)
.join(coordinador           ,   proyectos_table.c.Director_idDir ==   coordinador.c.idMiembro)
.join(proyec_conv_table     ,   proyec_conv_table.c.Proyec_idP   ==   proyectos_table.c.idProyec)
.join(convenios_table       ,   convenios_table.c.idConv         ==   proyec_conv_table.c.Conv_idC)
.join(estatus_table         ,   estatus_table.c.idEstatus        ==   proyectos_table.c.Estatus_idEst)
.join(cargos_coordinador    ,   coordinador.c.idCargo            ==   cargos_coordinador.c.idCargo)
.join(cargos_investigador   ,   investigador.c.idCargo           ==   cargos_investigador.c.idCargo)
.group_by(
    proyectos_table.c.idProyec,
    proyectos_table.c.Proyecto,
    estatus_table.c.Estatus,
    proyectos_table.c.Año_in,
    proyectos_table.c.Año_fin,
    coordinador.c.nombre,
    coordinador.c.apellido
)
)

def get_project(id):
    query=query_get_proyectos.where(proyectos_table.c.idProyec == id)
    json_data=get_data(section='projects',query=query)
    print(json_data)
    try:
        return Proyect(**json_data[0])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Project not found in database')

def get_insert_query_proyect(proyect:Proyect_db):
    query=get_insert_query(table=proyectos_table,params={'Proyecto':proyect.name,
                                                        'Estatus_idEst':proyect.id_status,
                                                        'Director_idDir':proyect.id_coordinator,
                                                        'Año_in':proyect.period.year_start,
                                                        'Año_fin':proyect.period.year_end})
    return query

def get_insert_query_coordinator(coordinator:Member):
    query=get_insert_query(table=miembros_table,params={'nombre':coordinator.first_name,'apellido':coordinator.last_name,'idCargo':coordinator.cargo.id})
    return query

def get_insert_query_researcher(researcher:Member):
    query=get_insert_query(table=miembros_table,params={'nombre':researcher.first_name,'apellido':researcher.last_name,'idCargo':researcher.cargo.id})
    return query

def get_insert_query_proyect_researcher(id_proyect:int,id_researcher:int):
    query=get_insert_query(table=proyec_invest_table,params={'Proyec_idP':id_proyect,'idMiembro':id_researcher})
    return query

def get_insert_querry_proyect_agreement(id_proyect:int,id_agreement:int):
    query=get_insert_query(table=proyec_conv_table,params={'Proyec_idP':id_proyect,'Conv_idC':id_agreement})
    return query

def get_insert_query_agreement(agreement:Agreement):
    query=get_insert_query(table=convenios_table,params={'Convenio':agreement.value})
    return query

def insert_proyect(proyect:Proyect_db):
    query=get_insert_query_proyect(proyect=proyect)
    id=execute_insert(query=query)
    return id

def insert_coordinator(coordinator:Member):
    query=get_insert_query_coordinator(coordinator=coordinator)
    id=execute_insert(query=query)
    return id

def insert_researcher(researcher:Member):
    query=get_insert_query_researcher(researcher=researcher)
    id=execute_insert(query=query)
    return id

def insert_proyect_researcher(id_proyect:int,id_researcher:int):
    query=get_insert_query_proyect_researcher(id_proyect=id_proyect,id_researcher=id_researcher)
    id=execute_insert(query=query)
    return id

def insert_agreement(agreement:Agreement):
    query=get_insert_query_agreement(agreement=agreement)
    id=execute_insert(query=query)
    return id

def insert_proyect_agreement(id_proyect:int,id_agreement:int):
    query=get_insert_querry_proyect_agreement(id_proyect=id_proyect,id_agreement=id_agreement)
    id=execute_insert(query=query)
    return id

def get_id_proyect(proyect:Proyect_db):
    id_proyect=get_id(table=proyectos_table,filters={'Proyecto':proyect.name},param='idProyec')

    if id_proyect is None:
        id_proyect=insert_proyect(proyect=proyect)
        return id_proyect
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail='Este proyecto ya está registrado')

def get_id_coordinator(coordinator:Member):
    if coordinator.id is None:
        id_coordinator=insert_coordinator(coordinator=coordinator)
        return id_coordinator

def get_id_researcher(researcher:Member):
    if researcher.id is None:
        id_researcher=insert_researcher(researcher=researcher)
        return id_researcher
    
    return id_researcher[0]

def get_id_agreement(agreement:Agreement):
    id_agreement=get_id(table=convenios_table,filters={'Convenio':agreement.value},param='idConv')

    if id_agreement is None:
        id_agreement=insert_agreement(agreement=agreement)
        return id_agreement

    return id_agreement[0]

def create_register_proyect(proyect:Proyect,user:User):

    #Registro del coordinador
    if proyect.coordinator.id is None:
        id_coordinator=insert_coordinator(coordinator=proyect.coordinator)
        proyect.coordinator.id=id_coordinator

    #Registro del proyecto

    proyect_db=Proyect_db(**scheme_proyect_to_db(proyect=proyect,id_coordinator=proyect.coordinator.id))

    id_proyect=get_id_proyect(proyect=proyect_db)

    proyect.id=id_proyect

    #Registro de los investigadores

    for researcher in proyect.researchers:
        if researcher.id is None:
            researcher_id=insert_researcher(researcher=researcher)
            researcher.id=researcher_id
        _=insert_proyect_researcher(id_proyect=proyect.id,id_researcher=researcher.id)
    
    #Registro de los convenios

    for agreement in proyect.agreements:
        if agreement.id is None:
            id_agreement=insert_agreement(agreement=agreement)
            agreement.id=id_agreement
        _=insert_proyect_agreement(id_proyect=proyect.id,id_agreement=agreement.id)
    
    create_record(id_user=user.id,username=user.user_name,section="proyect",action='create',new_data=proyect)

    return {
        "message":"Proyecto agregado"
    }

def update_name(id_proyect:int,name:str):
    query=get_update_query(table=proyectos_table,filters={'idProyec':id_proyect},params={'Proyecto':name})
    execute_update(query=query)

def update_coordinator(id_proyect:int,coordinator:Member):
    query=get_update_query(table=proyectos_table,filters={'idProyec':id_proyect},params={'Director_idDir':coordinator.id})
    execute_update(query=query)

def get_insert_querry_proyect_researcher(id_proyect:int,id_researcher:int):
    query=get_insert_query(table=proyec_invest_table,params={'Proyec_idP':id_proyect,'idMiembro':id_researcher})
    return query

def add_researcher(id_proyect:int,researcher:Member):
    query_insert_proyect_researcher=get_insert_query_proyect_researcher(id_proyect=id_proyect,id_researcher=researcher.id)
    _=execute_insert(query=query_insert_proyect_researcher)

def delete_researcher(id_proyect:int,id_reseracher:int):
    delete_query=(delete(proyec_invest_table)
                .where(proyec_invest_table.c.Proyec_idP == id_proyect,
                    proyec_invest_table.c.idMiembro == id_reseracher))
    execute_delete(query=delete_query)

def get_insert_querry_proyect_agreement(id_proyect:int,id_agreement:int):
    insert_query=insert(proyec_conv_table).values(
        Proyec_idP=id_proyect,
        Conv_idC=id_agreement
    )
    return insert_query

def add_agreement(id_proyect:int,agreement:Agreement):

    query_insert_proyect_agreement=get_insert_querry_proyect_agreement(id_proyect=id_proyect,id_agreement=agreement.id)

    _=execute_insert(query=query_insert_proyect_agreement)

    return agreement.id

def delete_agreement(id_proyect:int,id_agreement:int):
    query=get_delete_query(table=proyec_conv_table,params={'Proyec_idP':id_proyect,'Conv_idC':id_agreement})
    execute_delete(query=query)

def update_status(id_proyect:int,id_status:int):
    query=get_update_query(table=proyectos_table,filters={'idProyec':id_proyect},params={'Estatus_idEst':id_status})
    execute_update(query=query)

def update_date(id_proyect:int,param,year):
    query=get_update_query(table=proyectos_table,filters={'idProyec':id_proyect},params={param:year})
    execute_update(query=query)

def update_period(id_proyect:int,period:Period):
    if period.year_start is not None:
        update_date(id_proyect=id_proyect,param='Año_in',year=period.year_start)
    if period.year_end is not None:
        update_date(id_proyect=id_proyect,param='Año_fin',year=period.year_end)


def update_register_proyect(project:Proyect_update,user:User):

    previous_data=get_project(id=project.id)

    if project.name is not None:
        update_name(id_proyect=project.id,name=project.name)
    
    if project.coordinator is not None:
        if project.coordinator.id is None:
            id_coordinator=insert_coordinator(coordinator=project.coordinator)
            project.coordinator.id=id_coordinator
        update_coordinator(id_proyect=project.id,coordinator=project.coordinator)

    if len(project.researchers_added) != 0:
        for researcher in project.researchers_added:
            if researcher.id is None:
                id_researcher=insert_researcher(researcher=researcher)
                researcher.id=id_researcher
            add_researcher(id_proyect=project.id,researcher=researcher)
            
    if len(project.researchers_deleted) != 0:
        for researcher in project.researchers_deleted:
            delete_researcher(id_proyect=project.id,id_reseracher=researcher.id)
    
    if len(project.agreements_added) != 0:
        for agreement in project.agreements_added:
            if agreement.id is None:
                id_agreement=insert_agreement(agreement=agreement)
                agreement.id=id_agreement
            id_agreement=add_agreement(id_proyect=project.id,agreement=agreement)
            
    if len(project.agreements_deleted) != 0:
        for agreement in project.agreements_deleted:
            delete_agreement(id_proyect=project.id,id_agreement=agreement.id)
    if project.status is not None:
        update_status(id_proyect=project.id,id_status=project.status.id)
    if project.period is not None:
        update_period(id_proyect=project.id,period=project.period)

    create_record(id_user=user.id,username=user.user_name,section="projects",action='update',new_data=project,previous_data=previous_data)
    
    return {
        "response":"Proyect updated"
    }

def delete_id_proyect_researcher(id_proyect:int):
    delete_query=(delete(proyec_invest_table).where(
        proyec_invest_table.c.Proyec_idP == id_proyect,
    ))
    execute_delete(query=delete_query)

def delete_id_proyect_agreements(id_proyect:int):
    delete_query=(delete(proyec_conv_table).where(
        proyec_conv_table.c.Proyec_idP == id_proyect,
    ))
    execute_delete(query=delete_query)

def delete_proyect(id_proyect:int):
    delete_query=(delete(proyectos_table).where(
        proyectos_table.c.idProyec == id_proyect,
    ))
    execute_delete(query=delete_query)

def delete_register_proyect(id_proyect:int,user:User):

    previous_data=get_project(id=id_proyect)

    delete_id_proyect_researcher(id_proyect=id_proyect)
    delete_id_proyect_agreements(id_proyect=id_proyect)
    delete_proyect(id_proyect=id_proyect)
    create_record(id_user=user.id,username=user.user_name,section="projects",action='delete',previous_data=previous_data)
    return {
        "response":'Proyecto eliminado'
    }

