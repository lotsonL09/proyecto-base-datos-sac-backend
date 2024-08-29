from sqlalchemy import select

from db.schemas_tables.schemas_tables import estado_table,estatus_table

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from extra.schemas_function import scheme_status_db

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
    
