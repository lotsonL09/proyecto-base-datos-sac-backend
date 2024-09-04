from sqlalchemy import select

from db.schemas_tables.schemas_tables import ubicacion_table

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from extra.schemas_function import scheme_location_db

from entities.location import Location

querry_get_location=select(ubicacion_table)

Session=sessionmaker(engine)

def get_locations_data(query) -> list[Location]:
    all_locations=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for status in results:
            location_db=Location(**scheme_location_db(status))
            all_locations.append(location_db)
    return all_locations


