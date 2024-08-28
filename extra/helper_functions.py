from typing import Tuple

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from fastapi.encoders import jsonable_encoder

from db.db_session import engine

from db.querries.ubicacion import get_locations_data,querry_get_location

from db.querries.estados import query_get_status,get_status_data

from db.schemas_tables.schemas_tables import ubicacion_table,estado_table

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
                query=query_get_status.where(estado_table.c.IdEstado == value)
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

def get_id_query(table,param):
    return select(param).select_from(table)

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