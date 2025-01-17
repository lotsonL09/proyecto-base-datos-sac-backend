from fastapi import APIRouter,Depends

from sqlalchemy.orm import sessionmaker

from db.mysql_session.db_session import engine

from db.querries.libros import query_get_books
from db.querries.equipos import query_get_equipments,get_types_data
from db.querries.papers import query_get_papers
from db.querries.proyectos import query_get_proyectos
from db.querries.trabajos import query_get_trabajos
from db.querries.estados import query_get_status_book_equipment,get_status_data,query_get_status_proyect

from db.querries.ubicacion import query_get_location,get_locations_data
from db.querries.cursos import get_courses_data,query_get_courses
from db.querries.convenios import get_agreements_data,query_get_agreement
from db.querries.roles import get_roles_data,query_get_role
from db.querries.records import get_register_records
from db.querries.miembros import query_get_members,get_members_data

from db.querries.users import query_get_users

from extra.helper_functions import get_data

from config.auth import auth_user

home=APIRouter(prefix='/home')

Session=sessionmaker(engine)

#user=Depends(auth_user)

@home.get('/books')
async def get_books(user=Depends(auth_user)):
    query=query_get_books
    json_data=get_data(section='books',query=query)
    return json_data

@home.get('/equipments')
async def get_equipments(user=Depends(auth_user)):
    query=query_get_equipments
    json_data=get_data(section='equipments',query=query)
    return json_data

@home.get('/papers')
async def get_papers(user=Depends(auth_user)):
    query=query_get_papers
    json_data=get_data(section='papers',query=query)
    return json_data


@home.get('/projects')
async def get_proyectos(user=Depends(auth_user)):
    query=query_get_proyectos
    json_data=get_data(section='projects',query=query)
    return json_data


@home.get('/trabajos')
async def get_trabajos(user=Depends(auth_user)):
    query=query_get_trabajos
    json_data=get_data(section='trabajos',query=query)
    return json_data

@home.get('/users')
async def get_users(user=Depends(auth_user)):
    query=query_get_users
    result=get_data(section='users',query=query)
    return {
        "users":result
    }

@home.get('/records')
async def get_records(user=Depends(auth_user)):
    records=get_register_records(user_name=user.user_name)
    return records

@home.get('/status/book')
async def get_status():
    query=query_get_status_book_equipment
    result=get_status_data(query)
    return {
        "status":result
    }

@home.get('/status/equipment')
async def get_status():
    query=query_get_status_book_equipment
    result=get_status_data(query)
    return {
        "status":result
    }

@home.get('/status/project')
async def get_status():
    query=query_get_status_proyect
    result=get_status_data(query)
    return {
        "status":result
    }

@home.get('/locations')
async def get_locations():
    query=query_get_location
    result=get_locations_data(query)
    return {
        "locations":result
    }

@home.get('/courses')
async def get_locations():
    query=query_get_courses
    result=get_courses_data(query)
    return {
        "locations":result
    }

@home.get('/members')
async def get_members():
    query=query_get_members
    result=get_members_data(query=query)
    return result

@home.get('/equipment_type')
async def get_equiment_types():
    result=get_types_data()
    return {
        'equipment_types':result
    }

@home.get('/agreements')
async def get_agreements():
    query=query_get_agreement
    result=get_agreements_data(query)
    return {
        "agreements":result
    }

@home.get('/categories_user')
async def get_categories():
    query=query_get_role
    result=get_roles_data(query)
    return {
        "agreements":result
    }