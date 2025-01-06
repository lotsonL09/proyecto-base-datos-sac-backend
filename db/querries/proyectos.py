from fastapi import status,HTTPException

from sqlalchemy import Select,func,distinct,insert,delete

from db.schemas_tables.schemas_tables import (proyec_invest_table,proyectos_table,
                                            convenios_table,miembros_table,
                                            proyec_conv_table,estatus_table)

from extra.helper_functions import (execute_insert,execute_update,execute_delete,
                                    get_id,get_insert_query,get_update_query,
                                    get_delete_query,send_activity_record)

from entities.user import User

from extra.schemas_function import scheme_proyect_to_db

from entities.proyect import Proyect,Proyect_db,Agreement,Proyect_update,Period

from entities.share.shared import Member

coordinador=miembros_table.alias('coordinador')
investigador=miembros_table.alias('investigador')

query_get_proyectos=(Select(
    proyectos_table.c.idProyec,
    proyectos_table.c.Proyecto,
    func.concat(coordinador.c.idMiembro,';',coordinador.c.nombre,';',coordinador.c.apellido).label('Coordinador'),
    func.aggregate_strings(
        distinct(func.concat('(',investigador.c.idMiembro,',',investigador.c.nombre,',',investigador.c.apellido,')'))
            .op('ORDER BY')(func.concat('(',investigador.c.idMiembro,',',investigador.c.nombre,',',investigador.c.apellido,')')),
        ';'
    ).label('Investigadores'),
    func.aggregate_strings(
        distinct(convenios_table.c.Convenio)
            .op('ORDER BY')(convenios_table.c.Convenio),
        ';'
    ).label('Convenios'),
    estatus_table.c.Estatus,
    proyectos_table.c.Año_in,
    proyectos_table.c.Año_fin
)
.join(proyec_invest_table   ,   proyec_invest_table.c.Proyec_idP ==   proyectos_table.c.idProyec)
.join(investigador          ,   investigador.c.idMiembro         ==   proyec_invest_table.c.idMiembro)
.join(coordinador           ,   proyectos_table.c.Director_idDir ==   coordinador.c.idMiembro)
.join(proyec_conv_table     ,   proyec_conv_table.c.Proyec_idP   ==   proyectos_table.c.idProyec)
.join(convenios_table       ,   convenios_table.c.idConv         ==   proyec_conv_table.c.Conv_idC)
.join(estatus_table         ,   estatus_table.c.idEstatus        ==   proyectos_table.c.Estatus_idEst)
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


def get_insert_query_proyect(proyect:Proyect_db):
    query=get_insert_query(table=proyectos_table,params={'Proyecto':proyect.name,
                                                        'Estatus_idEst':proyect.id_status,
                                                        'Director_idDir':proyect.id_coordinator,
                                                        'Año_in':proyect.period.year_start.year,
                                                        'Año_fin':proyect.period.year_end.year})
    return query

def get_insert_query_coordinator(coordinator:Member):
    query=get_insert_query(table=miembros_table,params={'nombre':coordinator.first_name,'apellido':coordinator.last_name,'idCargo':4})
    return query

def get_insert_query_researcher(researcher:Member):
    query=get_insert_query(table=miembros_table,params={'nombre':researcher.first_name,'apellido':researcher.last_name,'idCargo':4})
    return query

def get_insert_query_proyect_researcher(id_proyect:int,id_researcher:int):
    query=get_insert_query(table=proyec_invest_table,params={'Proyec_idP':id_proyect,'idMiembro':id_researcher})
    return query

def get_insert_querry_proyect_agreement(id_proyect:int,id_agreement:int):
    query=get_insert_query(table=proyec_conv_table,params={'Proyec_idP':id_proyect,'Conv_idC':id_agreement})
    return query

def get_insert_query_agreement(agreement:Agreement):
    query=get_insert_query(table=convenios_table,params={'Convenio':agreement.name})
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
    id_coordinator=get_id(table=miembros_table,filters={'nombre':coordinator.first_name,'apellido':coordinator.last_name},param='idMiembro')
    if id_coordinator is None:
        id_coordinator=insert_coordinator(coordinator=coordinator)
        return id_coordinator
    else:
        return id_coordinator[0]

def get_id_researcher(researcher:Member):
    id_researcher=get_id(table=miembros_table,filters={'nombre':researcher.first_name,'apellido':researcher.last_name},param='idMiembro')
    
    if id_researcher is None:
        id_researcher=insert_researcher(researcher=researcher)
        return id_researcher
    
    return id_researcher[0]

def get_id_agreement(agreement:Agreement):
    id_agreement=get_id(table=convenios_table,filters={'Convenio':agreement.name},param='idConv')

    if id_agreement is None:
        id_agreement=insert_agreement(agreement=agreement)
        return id_agreement

    return id_agreement[0]

def create_register_proyect(proyect:Proyect,user:User):

    #Registro del coordinador

    id_coordinator=get_id_coordinator(proyect.coordinator)

    #Registro del proyecto

    proyect_db=Proyect_db(**scheme_proyect_to_db(proyect=proyect,id_coordinator=id_coordinator))

    id_proyect=get_id_proyect(proyect=proyect_db)

    #Registro de los investigadores

    id_researchers=[]

    for researcher in proyect.researchers:
        researcher_id=get_id_researcher(researcher=researcher)
        id_researchers.append(researcher_id)
    
    for id_resarcher in id_researchers:
        _=insert_proyect_researcher(id_proyect=id_proyect,id_researcher=id_resarcher)
    
    #Registro de los convenios

    id_agreements=[]

    for agreement in proyect.agreements:
        id_agreement=get_id_agreement(agreement=agreement)
        id_agreements.append(id_agreement)
    
    for id_agreement in id_agreements:
        _=insert_proyect_agreement(id_proyect=id_proyect,id_agreement=id_agreement)
    
    send_activity_record(id_user=user.id,section="projects",id_on_section=id_proyect,action="create")

    return {
        "message":"Proyecto agregado"
    }

def update_name(id_proyect:int,name:str):
    query=get_update_query(table=proyectos_table,filters={'idProyec':id_proyect},params={'Proyecto':name})
    execute_update(query=query)

def update_coordinator(id_proyect:int,coordinator:Member):
    id_coordinator=get_id_coordinator(coordinator=coordinator)
    query=get_update_query(table=proyectos_table,filters={'idProyec':id_proyect},params={'Director_idDir':id_coordinator})
    execute_update(query=query)
    return id_coordinator

def get_insert_querry_proyect_researcher(id_proyect:int,id_researcher:int):
    query=get_insert_query(table=proyec_invest_table,params={'Proyec_idP':id_proyect,'idMiembro':id_researcher})
    return query

def add_researcher(id_proyect:int,researcher:Member):
    id_researcher=get_id_researcher(researcher=researcher)
    query_insert_proyect_researcher=get_insert_query_proyect_researcher(id_proyect=id_proyect,id_researcher=id_researcher)
    _=execute_insert(query=query_insert_proyect_researcher)
    return id_researcher

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
    id_agreement=get_id_agreement(agreement=agreement)

    query_insert_proyect_agreement=get_insert_querry_proyect_agreement(id_proyect=id_proyect,id_agreement=id_agreement)

    _=execute_insert(query=query_insert_proyect_agreement)
    return id_agreement

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
        update_date(id_proyect=id_proyect,param='Año_in',year=period.year_start.year)
    if period.year_end is not None:
        update_date(id_proyect=id_proyect,param='Año_fin',year=period.year_end.year)


#TODO: HACER UNA VERIFICACION DE LA FECHA

def update_register_proyect(project:Proyect_update,user:User):

    if project.name is not None:
        update_name(id_proyect=project.id,name=project.name)
    
    coordinator_updated=None

    if project.coordinator is not None:
        id_coordiantor_updated=update_coordinator(id_proyect=project.id,coordinator=project.coordinator)

        coordinator_updated={
            "id":id_coordiantor_updated,
            "first_name":project.coordinator.first_name,
            "last_name":project.coordinator.last_name
        }

    researchers_updated=[]

    if len(project.researchers_added) != 0:
        for researcher in project.researchers_added:
            id_researcher=add_researcher(id_proyect=project.id,researcher=researcher)
            researchers_updated.append({
                "id":id_researcher,
                "first_name":researcher.first_name,
                "last_name":researcher.last_name
            })
    if len(project.researchers_deleted) != 0:
        for researcher in project.researchers_deleted:
            delete_researcher(id_proyect=project.id,id_reseracher=researcher.id)
    
    agreements_updated=[]

    if len(project.agreements_added) != 0:
        for agreement in project.agreements_added:
            id_agreement=add_agreement(id_proyect=project.id,agreement=agreement)
            agreements_updated.append({
                "id":id_agreement,
                "name":agreement.name
            })

    if len(project.agreements_deleted) != 0:
        for agreement in project.agreements_deleted:
            delete_agreement(id_proyect=project.id,id_agreement=agreement.id)
    if project.status is not None:
        update_status(id_proyect=project.id,id_status=project.status)
    if project.period is not None:
        update_period(id_proyect=project.id,period=project.period)

    send_activity_record(id_user=user.id,section="projects",id_on_section=project.id,action="update")
    
    return {
        "id":project.id,
        "coordinator":coordinator_updated,
        "researchers_added":researchers_updated,
        "agreements_added":agreements_updated
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
    delete_id_proyect_researcher(id_proyect=id_proyect)
    delete_id_proyect_agreements(id_proyect=id_proyect)
    delete_proyect(id_proyect=id_proyect)
    send_activity_record(id_user=user.id,section="projects",action="delete")
    return {
        "response":'Proyecto eliminado'
    }

