from sqlalchemy import Select,func
from db.schemas_tables.schemas_tables import (sections_table,actions_table,
                                            records_table,usuario_table)
from extra.helper_functions import (get_data)

from db.mongo_session.db_session import mongo_client

from entities.record import (Record_Book,Record_Equipment,Record_Paper,
                            Record_Project,Record_Trabajo,Record_User)

from entities.equipment import Equipment

from datetime import datetime,timezone

from pydantic import BaseModel

'''
Lo que se hizo para mysql

query_get_records=(Select(
    records_table.c.id_record,
    usuario_table.c.user_name,
    actions_table.c.message,
    sections_table.c.name,
    records_table.c.time,
    sections_table.c.table_name,
    records_table.c.id_on_section
    )
    .join(records_table,records_table.c.id_action == actions_table.c.id_action)
    .join(usuario_table,usuario_table.c.id_usuario == records_table.c.id_user)
    .join(sections_table,sections_table.c.id_section == records_table.c.id_section))


def get_records_user(user_name:str):
    query=query_get_records.where(usuario_table.c.user_name == user_name)
    return get_data(section='records',query=query)

'''

def create_record(id_user:int,username:str,section:str,action:str,previous_data:BaseModel=None,new_data:BaseModel=None,database:str='records'):
    #collection=mongo_client[f'{database}'][f'{username}']

    json_record={
        'user':{
            'idUser':id_user,
            'userName':username
        },
        'time':datetime.now(timezone.utc),
        'section':section,
        'action':action
    }
    
    match action:
        case 'create':
            json_record.update({
                'previousVersion':None,
                'newVersion':new_data.model_dump()
            })
        case 'update':
            json_record.update({
                'previousVersion':previous_data.model_dump(),
                'newVersion':new_data.model_dump()
            })
        case 'delete':
            json_record.update({
                'previousVersion':previous_data.model_dump(),
                'newVersion':None
            })

    mongo_client[f'{database}'][f'{username}'].insert_one(json_record)
    
