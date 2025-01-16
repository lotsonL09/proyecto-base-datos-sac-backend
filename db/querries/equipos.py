from fastapi import HTTPException,status

from sqlalchemy import Select,func,select

from db.schemas_tables.schemas_tables import (equipo_table,tipo_table,
                                            ubicacion_table,estado_table)

from extra.helper_functions import (get_id,get_insert_query,
                                    execute_insert)

from extra.helper_functions import (get_update_query,execute_update,execute_get,
                                    get_delete_query,execute_delete,
                                    get_data)

from entities.user import User

from entities.equipment import Equipment_Create,Type

from entities.location import Location

from sqlalchemy.orm import sessionmaker

from db.mysql_session.db_session import engine

from entities.status import Status

from db.querries.records import create_record

from extra.schemas_function import scheme_types_db

query_get_equipments=(Select(
        equipo_table.c.IdEquipo,
        equipo_table.c.Equipo,
        equipo_table.c.Descripcion,
        equipo_table.c.Evidencia,
        func.concat('(',tipo_table.c.IdTipo,';',tipo_table.c.Tipo,')'),
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

Session=sessionmaker(engine)

query_get_types_equipment=(select(tipo_table))

def get_types_data() -> list[Type]:
    all_types=[]
    with Session() as session:
        results=session.execute(query_get_types_equipment).fetchall()
        for role in results:
            role_db=Type(**scheme_types_db(role))
            all_types.append(role_db)
    return all_types

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

def insert_equipment(equipment:Equipment_Create):

    if equipment.type.id is None:
        id_type=get_id_type(type_name=equipment.type.value)
        equipment.type.id=id_type

    params=dict()

    if equipment.year is None:
        params={
            'Equipo':equipment.equipment,
            'Descripcion':equipment.description,
            'Evidencia':equipment.evidence,
            'Procedencia':equipment.origin,
            'Año_adquisicion': 'Indefinido',
            'IdTipo':equipment.type.id,
            'IdUbi':equipment.location.id,
            'IdEstado':equipment.status.id
        }
    else:
        params={
            'Equipo':equipment.equipment,
            'Descripcion':equipment.description,
            'Evidencia':equipment.evidence,
            'Procedencia':equipment.origin,
            'Año_adquisicion': equipment.year,
            'IdTipo':equipment.type.id,
            'IdUbi':equipment.location.id,
            'IdEstado':equipment.status.id
        }

    query=get_insert_query(table=equipo_table,params=params)
    id_equipment=execute_insert(query=query)

    return id_equipment

def get_equipment(id_equipment:int):
    query=query_get_equipments.where(equipo_table.c.IdEquipo == id_equipment)
    json_data=get_data(section='equipments',query=query)[0]
    if json_data:
        return Equipment_Create(**json_data)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Equipment not found in database')

def get_id_equipment(equipment:Equipment_Create):
    filters={'Equipo':equipment.equipment}
    id_equipment=get_id(table=equipo_table,param='IdEquipo',filters=filters)

    if id_equipment is None:
        id_equipment=insert_equipment(equipment=equipment)
        return id_equipment
    else:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail='Este equipo ya está registrado')

def create_register_equipment(equipment:Equipment_Create,user:User):

    id_equipment=get_id_equipment(equipment=equipment)

    equipment.id=id_equipment

    create_record(id_user=user.id,username=user.user_name,section="equipment",action='create',new_data=equipment)

    return {
        "message":"Equipo agregado"
    }

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

def update_type(id_equipment:int,type:Type) -> Type:
    id_type=type.id
    if id_type is None:
        id_type=get_id_type(type_name=type.value)
        type.id=id_type
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'IdTipo':id_type})
    execute_update(query=query)
    return type

def update_location(id_equipment:int,location:Location):
    id_location=location.id
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'IdUbi':id_location})
    execute_update(query=query)

def update_status(id_equipment:int,status:Status):
    id_status=status.id
    query=get_update_query(table=equipo_table,filters={'IdEquipo':id_equipment},params={'IdEstado':id_status})
    execute_update(query=query)

def update_register_equipment(equipment:Equipment_Create,user:User):

    previous_data=get_equipment(id_equipment=equipment.id)
    
    if equipment.equipment is not None:
        update_equipment_name(id_equipment=equipment.id,equipment_name=equipment.equipment)
    if equipment.description is not None:
        update_description(id_equipment=equipment.id,description=equipment.description)
    if equipment.evidence is not None:
        update_evidence(id_equipment=equipment.id,evidence=equipment.evidence)
    if equipment.origin is not None:
        update_origin(id_equipment=equipment.id,origin=equipment.origin)
    if equipment.year is not None:
        update_year(id_equipment=equipment.id,year=equipment.year)
    if equipment.type is not None:
        type_update=update_type(id_equipment=equipment.id,type=equipment.type)
        if equipment.type.id is None:
            equipment.type.id=type_update
    if equipment.location is not None:
        update_location(id_equipment=equipment.id,location=equipment.location)
    if equipment.status is not None:
        update_status(id_equipment=equipment.id,status=equipment.status)
    
    create_record(id_user=user.id,username=user.user_name,section="equipment",action='update',new_data=equipment,previous_data=previous_data)

    return {
        'response':'Equipo actualizado'
    }

def delete_register_equipment(id_equipment:int,user:User):
    previous_data=get_equipment(id_equipment=id_equipment)
    query=get_delete_query(table=equipo_table,params={'IdEquipo':id_equipment})
    execute_delete(query=query)
    #send_activity_record(id_user=user.id,section="equipments",action="delete")
    create_record(id_user=user.id,username=user.user_name,section="equipment",action='delete',previous_data=previous_data)
    return {
        'response':'Equipo eliminado'
    }


