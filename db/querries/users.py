from sqlalchemy import Select,insert,func,select,delete
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import usuario_table,roles_table

from db.mysql_session.db_session import engine

from extra.schemas_function import scheme_user,scheme_user_db

from entities.user import User_DB,User

from extra.helper_functions import (execute_get,get_insert_query,
                                    execute_insert,execute_update,
                                    get_update_query,execute_delete)

from db.querries.records import create_record

from db.mongo_session.db_session import mongo_client

Session=sessionmaker(engine)


query_get_users=(Select(
    usuario_table.c.id_usuario,
    usuario_table.c.user_name,
    usuario_table.c.first_name,
    usuario_table.c.last_name,
    usuario_table.c.email,
    usuario_table.c.id_role,
    roles_table.c.name,
    usuario_table.c.phone,
    usuario_table.c.disabled
).where(usuario_table.c.disabled == False)
.join(roles_table,usuario_table.c.id_role == roles_table.c.id)
.select_from(usuario_table))


"""
Column('id_usuario',Integer,primary_key=True,autoincrement=True),
    Column('user_name',String(100)),
    Column('password',String(100)),
    Column('first_name',String(100)),
    Column('last_name',String(100)),
    Column('email',String(100)),
    Column('category',String(50)),
    Column('phone',String(20)),
    Column('refresh_token',String(250)),
    Column('disabled',Boolean)
"""


def get_user_query(params:list,filter:dict) -> User|User_DB:
    
    columns_to_select=[getattr(usuario_table.c,param) for param in params]
    
    query=Select(*columns_to_select).select_from(usuario_table)

    for column,value in filter.items():
        query=query.where(getattr(usuario_table.c,column) == value)

    return query

user_column=['id_usuario','user_name','first_name','last_name',
                'email','id_role','phone','disabled']

user_db_column=['id_usuario','user_name','password','first_name',
                'last_name','email','id_role','phone','refresh_token','disabled']

def get_user_by_id(id:int):
    query=get_user_query(params=user_column,filter={'id_usuario':id})
    user_row=execute_get(query=query)
    if not user_row == None:

        id_role=user_row[5]
        role=get_role(id=id_role)
        user_row=list(user_row)
        user_row.insert(6,role)

        user_scheme=scheme_user(user_row=user_row)
        
        user_found=User(**user_scheme)
        return user_found
    else:
        return 'User not found'

def get_user_by_email(email:str):
    query=get_user_query(params=user_column,filter={'email':email})
    user_row=execute_get(query=query)
    if not user_row == None:
        user_scheme=scheme_user(user_row=user_row)
        user_found=User(**user_scheme)
        return user_found
    else:
        return 'User not found'

def get_user(field:str,value):
    query=get_user_query(params=user_column,filter={field:value})
    user_row=execute_get(query=query)

    if not user_row == None:

        id_role=user_row[5]
        role=get_role(id=id_role)
        user_row=list(user_row)
        user_row.insert(6,role)

        user_scheme=scheme_user(user_row=user_row)
        user_found=User(**user_scheme)
        
        return user_found
    else:
        return 'User not found'

def get_role(id):
    query=select(roles_table).where(roles_table.c.id == id)
    role=execute_get(query=query)[1]
    return role

def get_user_db(user_name:str):
    query=get_user_query(params=user_db_column,filter={'user_name':user_name})
    user_row=list(execute_get(query=query))
    id_role=user_row[6]
    role=get_role(id=id_role)
    user_row.insert(7,role)
    if not user_row == None:
        user_scheme=scheme_user_db(user_row=user_row)
        user_found=User_DB(**user_scheme)
        return user_found
    else:
        return 'User not found'

def insert_user(user:User_DB):
    params={
        "user_name":user.user_name,
        "password":user.password,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
        "id_role":user.role.id,
        "phone":user.phone,
        "refresh_token":user.refresh_token,
        "disabled":user.disabled
    }
    query=get_insert_query(table=usuario_table,params=params)
    _=execute_insert(query=query)
    inserted_user=get_user(field="user_name",value=user.user_name)

    #create_record(id_user=main_user.id,username=main_user.user_name,section="usuarios",action='create',new_data=inserted_user)

    return inserted_user

def update_password(id_user:int,password:str):
    query=get_update_query(table=usuario_table,filters={"id_usuario":id_user},params={"password":password})
    execute_update(query=query)

def update_user_field(id_user:int,field:str ,value:str):
    query=get_update_query(table=usuario_table,filters={'id_usuario':id_user},params={field:value})
    execute_update(query=query)

def update_register_user(user:User,collection:str):

    previous_data=get_user_by_id(id=user.id)

    if user.user_name is not None:
        update_user_field(id_user=user.id,field='user_name',value=user.user_name)

        mongo_client["records"][previous_data.user_name].rename(new_name=user.user_name)

    if user.first_name is not None:
        update_user_field(id_user=user.id,field='first_name',value=user.first_name)
    if user.last_name is not None:
        update_user_field(id_user=user.id,field='last_name',value=user.last_name)
    if user.email is not None:
        update_user_field(id_user=user.id,field='email',value=user.email)
    if user.role is not None:
        update_user_field(id_user=user.id,field='id_role',value=user.role.id)
    if user.phone is not None:
        update_user_field(id_user=user.id,field='phone',value=user.phone)
    
    create_record(id_user=user.id,username=collection,section="users",action='update',new_data=user,previous_data=previous_data)

    return {
        'response':'User updated'
    }

def delete_user(id:int):
    delete_query=(delete(usuario_table).where(
        usuario_table.c.id_usuario == id,
    ))
    execute_delete(query=delete_query)

def delete_register_user(id_user:int,user:User):

    previous_data=get_user_by_id(id=id_user)

    delete_user(id=id_user)

    create_record(id_user=user.id,username=user.user_name,section="users",action='delete',previous_data=previous_data)

    return {
        "response":'User eliminado'
    }
