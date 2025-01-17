from typing import Tuple

from sqlalchemy import select,text,insert,update,delete

from sqlalchemy.orm import sessionmaker

from fastapi.encoders import jsonable_encoder

from db.mysql_session.db_session import engine

from extra.schemas_function import (scheme_trabajo,scheme_equipment,
                                    scheme_book,scheme_user,scheme_paper,
                                    scheme_project,scheme_record)

from db.schemas_tables.schemas_tables import records_table

import jwt

from config.config import settings

from config.mail import mail,create_message

from datetime import datetime,timedelta,timezone

from datetime import datetime

import cloudinary.uploader

Session=sessionmaker(engine)

columns_data={
    'books':['id','title','authors','location','status','amount'],
    'equipments':['id','equipment','description','evidence','type','origin','year','location','status'],
    'papers':['id','title','members','year','link'],
    'projects':['id','project','coordinator','researchers','agreement','status','period'],
    'trabajos':['id','title','course','year','link']
}

queries_data={
    
}

cloudinary.config(
    cloud_name='dseolgqh1',
    api_key='322411164772336',
    api_secret='CPS76vFQEXOh26K2IEclNAY7HE8',
    secure=True
)

def upload_to_cloudinary(image,equipment_name:str) -> list[str]:

    date=datetime.now()

    public_id=f"{equipment_name}_evidence_{date}"

    response_cloud=cloudinary.uploader.upload(image,
                        public_id=public_id,
                        folder="evidencia_equipos")
    url_file=response_cloud["secure_url"]

    return url_file

def get_json(section:str,data:Tuple):
    if section == 'books':
        return scheme_book(params=columns_data[section],book_row=data)
    if section == 'equipments':
        return scheme_equipment(params=columns_data[section],equipment_row=data)
    if section == 'papers':
        return scheme_paper(params=columns_data[section],paper_row=data)
    if section == 'projects':
        return scheme_project(params=columns_data[section],project_row=data)
    if section == 'trabajos':
        return scheme_trabajo(trabajo_row=data)
    if section == 'users':
        return scheme_user(data)


def get_data(section:str,query):
    with Session() as session:
        data=session.execute(query).fetchall()
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

def get_update_query(table,filters:dict,params:dict):
    query=update(table)
    for column_name,value in filters.items():
        query=query.where(getattr(table.c,column_name) == value)
    query=query.values(**params)
    return query

def get_delete_query(table:str,params:dict):
    query=delete(table)
    for colum_name,value in params.items():
        query=query.where(getattr(table.c,colum_name) == value)
    return query

def execute_get(query):
    with Session() as session:
        result=session.execute(query).first()
        return result

def execute_get_all(query):
    with Session() as session:
        result=session.execute(query).fetchall()
        return result

def execute_insert(query):
    with Session() as session:
        register_inserted=session.execute(query)
        session.commit()
        id=register_inserted.inserted_primary_key[0]
    return id

def execute_update(query):
    with Session() as session:
        result=session.execute(query)
        session.commit()

def execute_delete(query):
    with Session() as session:
        session.execute(query)
        session.commit()

def create_access_token(subject:str,expire_delta:int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    expire=datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload={
        "sub":subject,
        "exp":expire,
        "mode":"access_token"
    }
    token=jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def create_refresh_token(subject:str,expire_delta:int=settings.REFRESH_TOKEN_EXPIRE_MINUTES):
    expire=datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload={
        "sub":subject,
        "exp":expire,
        "mode":"refresh_token"
    }
    token=jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

async def send_message(subject:str,body:str,recipients:list):

    message=create_message(recipients=recipients,
                        subject=subject,
                        body=body)
    
    await mail.send_message(message=message)

actions={
    "create":1,
    "update":2,
    "delete":3
}
sections={
    "books":1,
    "papers":2,
    "equipments":3,
    "projects":4,
    "trabajos":5,
    "users":6
}

def send_activity_record(id_user,section,action,id_on_section=None):

    time_now=datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    params_records={"id_user":id_user,
                    "id_section":sections[section],
                    "id_action":actions[action],
                    "id_on_section":id_on_section,
                    "time":time_now}
    
    query=get_insert_query(table=records_table,params=params_records)
    
    _=execute_insert(query=query)
