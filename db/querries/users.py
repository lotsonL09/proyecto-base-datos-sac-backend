from sqlalchemy import Select,insert
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import usuario_table

from db.db_session import engine

from extra.schemas_function import scheme_user,scheme_user_db

from entities.user import User_DB,User

from extra.helper_functions import execute_get,get_insert_query,execute_insert

Session=sessionmaker(engine)


def get_user_query(params:list,filter:dict) -> User|User_DB:
    
    columns_to_select=[getattr(usuario_table.c,param) for param in params]
    
    query=Select(*columns_to_select).select_from(usuario_table)

    for column,value in filter.items():
        query=query.where(getattr(usuario_table.c,column) == value)

    return query

user_column=['id_usuario','user_name','first_name','last_name',
                'email','category','phone','disabled']

user_db_column=['id_usuario','user_name','password','first_name',
                'last_name','email','category','phone','refresh_token','disabled']


def get_user_by_id(id:int):
    query=get_user_query(params=user_column,filter={'id_usuario':id})
    user_row=execute_get(query=query)
    if not user_row == None:
        user_scheme=scheme_user(user_row=user_row)
        user_found=User(**user_scheme)
        return user_found
    else:
        return 'User not found'

def get_user(user_name:str):
    query=get_user_query(params=user_column,filter={'user_name':user_name})
    user_row=execute_get(query=query)
    if not user_row == None:
        user_scheme=scheme_user(user_row=user_row)
        user_found=User(**user_scheme)
        
        return user_found
    else:
        return 'User not found'

def get_user_db(user_name:str):
    query=get_user_query(params=user_db_column,filter={'user_name':user_name})
    user_row=execute_get(query=query)
    if not user_row == None:
        user_scheme=scheme_user_db(user_row=user_row)
        user_found=User_DB(**user_scheme)
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
        refresh_token=user.refresh_token,
        disabled=user.disabled
    )
    return insert_querry


def insert_user(user:User_DB):
    params={
        "user_name":user.user_name,
        "password":user.password,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
        "category":user.category,
        "phone":user.phone,
        "refresh_token":user.refresh_token,
        "disabled":user.disabled
    }
    query=get_insert_query(table=usuario_table,params=params)
    _=execute_insert(query=query)
    inserted_user=get_user_db(user.user_name)
    return inserted_user

