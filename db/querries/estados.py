from sqlalchemy import select

from db.schemas_tables.schemas_tables import estado_table,estatus_table

from sqlalchemy.orm import sessionmaker

from db.mysql_session.db_session import engine

from extra.schemas_function import scheme_status_db

from extra.helper_functions import execute_get

from entities.status import Status

query_get_status_book_equipment=select(estado_table)
query_get_status_proyect=select(estatus_table)

Session=sessionmaker(engine)

def get_status_data(query) -> list[Status]:
    all_status=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for status in results:
            status_db=Status(**scheme_status_db(status))
            all_status.append(status_db)
    return all_status

def get_status_project(id):

    return

def get_status_book_equipment(id) ->Status:
    query=query_get_status_book_equipment.where(estado_table.c.IdEstado == id)
    result=execute_get(query=query)
    status_data=Status(**scheme_status_db(status_row=result))
    return status_data