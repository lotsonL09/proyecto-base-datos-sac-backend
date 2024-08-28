from fastapi import status,HTTPException
from sqlalchemy import Select,func,distinct,insert

from db.schemas_tables.schemas_tables import proyec_invest_table,proyectos_table,convenios_table,miembros_table,proyec_conv_table
from db.schemas_tables.schemas_tables import estatus_table

from extra.helper_functions import get_id_query,execute_get,execute_insert
from extra.schemas_function import scheme_proyect_to_db

from entities.proyect import Proyect,Proyect_db,Agreement

from entities.share.shared import Person

coordinador=miembros_table.alias('coordinador')
investigador=miembros_table.alias('investigador')

querry_get_proyectos=(Select(
    proyectos_table.c.idProyec,
    proyectos_table.c.Proyecto,
    func.concat(coordinador.c.nombre,' ',coordinador.c.apellido).label('Coordinador'),
    func.aggregate_strings(
        distinct(func.concat(investigador.c.nombre,' ',investigador.c.apellido))
            .op('ORDER BY')(func.concat(investigador.c.nombre,' ',investigador.c.apellido)),
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

query_get_id_proyect=get_id_query(table=proyectos_table,param=proyectos_table.c.Proyecto)

query_get_id_coordinator=get_id_query(table=miembros_table,param=miembros_table.c.idMiembro)

query_get_id_researcher=query_get_id_coordinator

query_get_id_agreement=get_id_query(table=convenios_table,param=convenios_table.c.idConv)

def get_insert_query_proyect(proyect:Proyect_db):
    insert_query=insert(proyectos_table).values(
    Proyecto=proyect.name,
    Estatus_idEst=proyect.id_status,
    Director_idDir=proyect.id_coordinator,
    Año_in=proyect.period.year_start.year,
    Año_fin=proyect.period.year_end.year
    )
    return insert_query

def get_insert_query_coordinator(coordinator:Person):
    insert_query=insert(miembros_table).values(
        nombre=coordinator.first_name,
        apellido=coordinator.last_name,
        idCargo = 4
    )
    return insert_query

def get_insert_query_researcher(researcher:Person):
    insert_query=insert(miembros_table).values(
        nombre=researcher.first_name,
        apellido=researcher.last_name,
        idCargo = 4
    )
    return insert_query

def get_insert_query_proyect_researcher(id_proyect:int,id_researcher:int):
    insert_query=insert(proyec_invest_table).values(
        Proyec_idP=id_proyect,
        idMiembro=id_researcher
    )
    return insert_query

def get_insert_querry_proyect_agreement(id_proyect:int,id_agreement:int):
    insert_query=insert(proyec_conv_table).values(
        Proyec_idP=id_proyect,
        Conv_idC=id_agreement
    )
    return insert_query

def get_insert_query_agreement(agreement:Agreement):
    insert_query=insert(convenios_table).values(
        Convenio=agreement.name
    )
    return insert_query

def insert_proyect(proyect:Proyect_db):
    query=get_insert_query_proyect(proyect=proyect)
    id=execute_insert(query=query)
    return id

def insert_coordinator(coordinator:Person):
    query=get_insert_query_coordinator(coordinator=coordinator)
    id=execute_insert(query=query)
    return id

def insert_researcher(researcher:Person):
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
    query=query_get_id_proyect.where(proyectos_table.c.Proyecto == proyect.name)

    id_proyect=execute_get(query=query)

    if id_proyect is None:
        id_proyect=insert_proyect(proyect=proyect)
        return id_proyect
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail='Este proyecto ya está registrado')

def get_id_coordinator(coordinator:Person):
    query=query_get_id_coordinator.where((miembros_table.c.nombre == coordinator.first_name) & 
                                        (miembros_table.c.apellido  == coordinator.last_name))
    
    id_coordinator=execute_get(query)

    if id_coordinator is None:
        id_coordinator=insert_coordinator(coordinator=coordinator)
        return id_coordinator
    else:
        return id_coordinator[0]

def get_id_researcher(researcher:Person):
    query=query_get_id_researcher.where((miembros_table.c.nombre == researcher.first_name) & 
                                        (miembros_table.c.apellido  == researcher.last_name))
    
    id_researcher=execute_get(query=query)

    if id_researcher is None:
        id_researcher=insert_researcher(researcher=researcher)
        return id_researcher
    
    return id_researcher

def get_id_agreement(agreement:Agreement):
    query=query_get_id_agreement.where(convenios_table.c.Convenio == agreement.name)

    id_agreement=execute_get(query=query)
    
    if id_agreement is None:
        id_agreement=insert_agreement(agreement=agreement)
        print(f'Id agreement added {id_agreement}')
        return id_agreement

    print(f'Id agreement added {id_agreement}')

    return id_agreement

def create_register_proyect(proyect:Proyect):

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
        
    return 'Registro realizado'





