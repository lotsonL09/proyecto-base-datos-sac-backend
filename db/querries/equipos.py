from fastapi import HTTPException,status

from sqlalchemy import Select,func

from db.schemas_tables.schemas_tables import equipo_table,tipo_table,ubicacion_table,estado_table

from extra.helper_functions import get_id,get_insert_query,execute_insert
from extra.helper_functions import get_update_query,execute_update,get_delete_query,execute_delete

from entities.equipment import Equipment

querry_get_equipments=(Select(
        equipo_table.c.IdEquipo,
        equipo_table.c.Equipo,
        equipo_table.c.Descripcion,
        equipo_table.c.Evidencia,
        tipo_table.c.Tipo,
        equipo_table.c.Procedencia,
        equipo_table.c.Año_adquisicion,
        func.concat('(',ubicacion_table.c.IdUbi,';',ubicacion_table.c.ubicacion,')'),
        func.concat('(',estado_table.c.IdEstado,';',estado_table.c.estado,')')
    )
    .select_from(equipo_table)
    .join(tipo_table        ,tipo_table.c.IdTipo       ==    equipo_table.c.IdTipo)
    .join(ubicacion_table   ,ubicacion_table.c.IdUbi   ==    equipo_table.c.IdUbi)
    .join(estado_table      ,estado_table.c.IdEstado   ==    equipo_table.c.IdEstado)
    )



def insert_type(type_name:str):
    params={'Tipo':type_name}
    query=get_insert_query(table=tipo_table,params=params)
    id=execute_insert(query=query)
    return id

def get_id_type(type_name:str):
    filters={'Tipo':type_name}
    id_type=get_id(table=tipo_table,filters=filters,param='IdTipo')
    if id_type is None:
        id_type=insert_type(type_name=type_name)
        return id_type
    return id_type[0]

def insert_equipment(equipment:Equipment):

    id_type=get_id_type(type_name=equipment.type)

    params=dict()

    if equipment.year is None:
        params={
            'Equipo':equipment.equipment,
            'Descripcion':equipment.description,
            'Evidencia':equipment.evidence,
            'Procedencia':equipment.origin,
            'Año_adquisicion': 'Indefinido',
            'IdTipo':id_type,
            'IdUbi':equipment.location,
            'IdEstado':equipment.status
        }
    else:
        params={
            'Equipo':equipment.equipment,
            'Descripcion':equipment.description,
            'Evidencia':equipment.evidence,
            'Procedencia':equipment.origin,
            'Año_adquisicion': equipment.year.year,
            'IdTipo':id_type,
            'IdUbi':equipment.location,
            'IdEstado':equipment.status
        }

    query=get_insert_query(table=equipo_table,params=params)
    id_equipment=execute_insert(query=query)

    return id_equipment

def get_id_equipment(equipment:Equipment):
    filters={'Equipo':equipment.equipment}
    id_equipment=get_id(table=equipo_table,param='IdEquipo',filters=filters)

    if id_equipment is None:
        id_equipment=insert_equipment(equipment=equipment)
        return id_equipment
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail='Este equipo ya está registrado')

def create_register_equipment(equipment:Equipment):

    _=get_id_equipment(equipment=equipment)

    return 'Registro realizado'

def update_equipment_name(id_equipment:int,equipment_name:str):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'Equipo':equipment_name})
    execute_update(query=query)

def update_description(id_equipment:int,description:str):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'Descripcion':description})
    execute_update(query=query)

def update_evidence(id_equipment:int,evidence:str):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'Evidencia':evidence})
    execute_update(query=query)

def update_origin(id_equipment:int,origin:str):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'Procedencia':origin})
    execute_update(query=query)

def update_year(id_equipment:int,year):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'Año_adquisicion':year})
    execute_update(query=query)

def update_type(id_equipment:int,type_name:int):
    id_type=get_id_type(type_name=type_name)
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'IdTipo':id_type})
    execute_update(query=query)

def update_location(id_equipment:int,id_location:int):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'IdUbi':id_location})
    execute_update(query=query)

def update_status(id_equipment:int,id_status:int):
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'IdEstado':id_status})
    execute_update(query=query)


def update_register_equipment(equipment:Equipment):
    
    if equipment.equipment is not None:
        update_equipment_name(id_equipment=equipment.id,equipment_name=equipment.equipment)
    if equipment.description is not None:
        update_description(id_equipment=equipment.id,description=equipment.description)
    if equipment.evidence is not None:
        update_evidence(id_equipment=equipment.id,evidence=equipment.evidence)
    if equipment.origin is not None:
        update_origin(id_equipment=equipment.id,origin=equipment.origin)
    if equipment.year is not None:
        update_year(id_equipment=equipment.id,year=equipment.year.year)
    if equipment.type is not None:
        update_type(id_equipment=equipment.id,type_name=equipment.type)
    if equipment.location is not None:
        update_location(id_equipment=equipment.id,id_location=equipment.location)
    if equipment.status is not None:
        update_status(id_equipment=equipment.id,id_status=equipment.status)
    
    return {
        'response':'Equipo actualizado'
    }

def delete_register_equipment(id_equipment:int):
    query=get_delete_query(table=equipo_table,params={'IdEquipo':id_equipment})
    execute_delete(query=query)
    return {
        'response':'Equipo eliminado'
    }


