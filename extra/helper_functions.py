from typing import Tuple

from sqlalchemy import select,text,insert,update,delete
from sqlalchemy.orm import sessionmaker

from fastapi.encoders import jsonable_encoder

from db.db_session import engine

from db.querries.ubicacion import get_locations_data,querry_get_location

from db.querries.estados import query_get_status_book_equipment,get_status_data

from db.schemas_tables.schemas_tables import ubicacion_table,estado_table

import jwt

from config import settings

from datetime import datetime,timedelta,timezone

Session=sessionmaker(engine)


columns_data={
    'books':['id','title','author','location','status','borrowed_to'],
    'equipments':['id','Description','type','origin','year','location','status'],
    'papers':['id','title','members','year','link'],
    'projects':['id','project','coordinator','researches','agreement','status','year_start','year_end'],
    'trabajos':['id','title','course','year','link']
}

#HACER DESPUES EL DE MIEMBROS

def get_json(section:str,data:Tuple):
    columns=columns_data[section]
    dict_json={}
    for key,value in zip(columns,data):
        if type(value) is not str:
            dict_json[key]=value
            if key == 'location':
                query=querry_get_location.where(ubicacion_table.c.IdUbi == value)
                location=get_locations_data(querry=query)[0]
                dict_json[key]={
                    'id':location.id,
                    "value":location.value
                }

            if key == 'status':
                query=query_get_status_book_equipment.where(estado_table.c.IdEstado == value)
                status=get_status_data(querry=query)[0]
                dict_json[key]={
                    'id':status.id,
                    "value":status.value
                }
        else:
            if key=='author' and (len(value.split(';')) == 1):
                dict_json[key]=[value]
                continue
            if len(value.split(';')) > 1:
                dict_json[key]=value.split(';')[:-1]
            else:
                dict_json[key]=value
    return dict_json

def get_data(section:str,querry):
    with Session() as session:
        data=session.execute(querry).fetchall()
    json_all=[]
    for register in data:
        register_json=get_json(section,register)
        json_all.append(register_json)
    return jsonable_encoder(json_all)

#TODO: Eliminar luego
def get_id_query(table,param):
    return select(param).select_from(table)

def get_id(table,filters:dict,param=None):
    query=None
    if param is None:
        query=select(table).select_from(table)
    else:
        query=select(text(param)).select_from(table)

    #query=query.where(**filters)
    for colum_name, value in filters.items():
        query=query.where(getattr(table.c,colum_name)==value)

    id=execute_get(query=query)

    return id

def get_insert_query(table,params:dict):
    query=insert(table).values(**params)
    return query

def get_update_query(table,filters,params):
    query=update(table)
    for column_name,value in filters:
        query=query.where(getattr(table.c,column_name) == value)
    query.values(**params)
    return query

def get_delete_query(table:str,params:dict):
    query=delete(table)
    for colum_name,value in params.items():
        query=query.where(getattr(table.c,colum_name) == value)
    return query

def execute_get(query):
    with Session() as session:
        id=session.execute(query).first()
        return id

def execute_insert(query):
    with Session() as session:
        register_inserted=session.execute(query)
        session.commit()
        id=register_inserted.inserted_primary_key[0]
    return id

def execute_update(query):
    with Session() as session:
        session.execute(query)
        session.commit()

def execute_delete(query):
    with Session() as session:
        session.execute(query)
        session.commit()

def create_access_token(subject:str,expire_delta:int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    expire=datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload={
        "sub":subject,
        "exp":expire
    }
    token=jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def create_refresh_access_token(subject:str,expire_delta:int=settings.REFRESH_TOKEN_EXPIRE_MINUTES):
    expire=datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload={
        "sub":subject,
        "exp":expire
    }
    token=jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token