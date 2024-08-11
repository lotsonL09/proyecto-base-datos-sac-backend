from typing import Tuple
from db.db_session import engine
from sqlalchemy.orm import sessionmaker
from flask import jsonify
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
    return jsonify(json_all)
