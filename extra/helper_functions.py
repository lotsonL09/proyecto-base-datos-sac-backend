from typing import Tuple

from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from fastapi.encoders import jsonable_encoder

from db.db_session import engine
from db.schemas_tables.schemas_tables import usuario_table
from db.querries.users import querry_get_users,querry_get_users_db
from db.schemas_tables.schemas_tables import usuario_table

from extra.schemas_function import scheme_user,scheme_user_db

from entities.user import User_DB,User

Session=sessionmaker(engine)

columns_data={
    'books':['Título','Autor','Ubicación','Estado','Prestado a'],
    'equipments':['Descripción','Tipo','Procedencia','Año de adquisición','Ubicación','Estado'],
    'papers':['Título','Miembros','Año','Link'],
    'proyects':['Proyecto','Coordinador UDEP','Investigadores UDEP','Convenio','Estado','Año de Inicio','Año de Finalización'],
    'trabajos':['Título','Curso','Año','Link']
}

#HACER DESPUES EL DE MIEMBROS

def get_json(section:str,data:Tuple):
    columns=columns_data[section]
    dict_json={}
    for key,value in zip(columns,data):
        if type(value) is not str:
            dict_json[key]=value
        else:
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


def get_user(user_name:str):
    with Session() as session:
        querry=querry_get_users.where(usuario_table.c.user_name == user_name)
        user_row=session.execute(querry).first()
        
        if not user_row == None:
            user_scheme=scheme_user(user_row=user_row)

            user_found=User(**user_scheme)

            return user_found
        else:
            return 'User not found'

def get_insert_querry_user(user:User_DB):
    insert_querry=insert(usuario_table).values(
        user_name=user.user_name,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        category=user.category,
        phone=user.phone,
        disabled=user.disabled
    )
    return insert_querry


def insert_user(user:User_DB):
    querry=get_insert_querry_user(user)

    with Session() as session:
        result=session.execute(querry)
        session.commit()

    inserted_user=get_user(user.user_name)

    return inserted_user

def search_on_db(user_name:str):
    with Session() as session:
        querry=querry_get_users_db.where(usuario_table.c.user_name == user_name)
        user_row=session.execute(querry).first()
        
        if not user_row == None:
            user_scheme=scheme_user_db(user_row=user_row)
            user_found=User_DB(**user_scheme)
            return user_found
        else:
            return 'User not found'