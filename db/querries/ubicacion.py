from sqlalchemy import select

from fastapi import HTTPException,status

from db.schemas_tables.schemas_tables import ubicacion_table

from sqlalchemy.orm import sessionmaker

from db.mysql_session.db_session import engine

from extra.schemas_function import scheme_location_db

from entities.location import Location

from extra.helper_functions import execute_get

query_get_location=select(ubicacion_table)

Session=sessionmaker(engine)

def get_locations_data(query) -> list[Location]:
    all_locations=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for status in results:
            location_db=Location(**scheme_location_db(status))
            all_locations.append(location_db)
    return all_locations

def get_location(id_location:int):
    query=execute_get(query=query_get_location.where(ubicacion_table.c.IdUbi == id_location))
    result=execute_get(query=query)
    if result is not None:
        location_db=Location(**scheme_location_db(result))
        return location_db
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Location not found')