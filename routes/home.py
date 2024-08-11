from flask import Blueprint,jsonify
from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from db.querries.libros import querry_get_books
from db.querries.equipos import querry_get_equipments
from db.querries.papers import querry_get_papers
from db.querries.proyectos import querry_get_proyectos
from db.querries.trabajos import querry_get_trabajos

from extra.helper_functions import get_data

home_bp=Blueprint('home',__name__,url_prefix='/home')

Session=sessionmaker(engine)


@home_bp.route('/libros',methods=['GET'])
def get_books():
    query=querry_get_books
    json_data=get_data(section='books',querry=query)
    return json_data

@home_bp.route('/equipos',methods=['GET'])
def get_equipments():
    query=querry_get_equipments
    json_data=get_data(section='equipments',querry=query)
    return json_data

@home_bp.route('/papers',methods=['GET'])
def get_papers():
    query=querry_get_papers
    json_data=get_data(section='papers',querry=query)
    return json_data


@home_bp.route('/proyectos',methods=['GET'])
def get_proyectos():
    query=querry_get_proyectos
    json_data=get_data(section='proyects',querry=query)
    return json_data


@home_bp.route('/trabajos',methods=['GET'])
def get_trabajos():
    query=querry_get_trabajos
    json_data=get_data(section='trabajos',querry=query)
    return json_data
