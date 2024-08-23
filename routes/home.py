from fastapi import APIRouter

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from db.querries.libros import querry_get_books
from db.querries.equipos import querry_get_equipments
from db.querries.papers import querry_get_papers
from db.querries.proyectos import querry_get_proyectos
from db.querries.trabajos import querry_get_trabajos
from db.querries.estados import querry_get_status,get_status_data

from db.querries.ubicacion import querry_get_location,get_locations_data

from extra.helper_functions import get_data

home=APIRouter(prefix='/home')

Session=sessionmaker(engine)


@home.get('/books')
async def get_books():
    query=querry_get_books
    json_data=get_data(section='books',querry=query)
    return json_data

@home.get('/equipments')
async def get_equipments():
    query=querry_get_equipments
    json_data=get_data(section='equipments',querry=query)
    return json_data

@home.get('/papers')
async def get_papers():
    query=querry_get_papers
    json_data=get_data(section='papers',querry=query)
    return json_data


@home.get('/projects')
async def get_proyectos():
    query=querry_get_proyectos
    json_data=get_data(section='projects',querry=query)
    return json_data


@home.get('/trabajos')
async def get_trabajos():
    query=querry_get_trabajos
    json_data=get_data(section='trabajos',querry=query)
    return json_data

@home.get('/status')
async def get_status():
    query=querry_get_status
    result=get_status_data(query)
    return result


@home.get('/locations')
async def get_locations():
    query=querry_get_location
    result=get_locations_data(query)
    return result