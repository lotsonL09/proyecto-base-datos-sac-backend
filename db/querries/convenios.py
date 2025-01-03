from sqlalchemy import select

from db.schemas_tables.schemas_tables import convenios_table

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from extra.schemas_function import scheme_agreement_db

from entities.location import Location

from entities.proyect import Agreement

querry_get_agreement=select(convenios_table)

Session=sessionmaker(engine)

def get_agreements_data(query) -> list[Location]:
    all_agreements=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for agreement in results:
            agreement_db=Agreement(**scheme_agreement_db(agreement))
            all_agreements.append(agreement_db)
    return all_agreements


