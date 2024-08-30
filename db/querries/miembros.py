from sqlalchemy import Select

from db.schemas_tables.schemas_tables import miembros_table

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from extra.schemas_function import scheme_member_db

from entities.share.shared import Member

Session=sessionmaker(engine)

query_get_members=Select(
    miembros_table.c.idMiembro,
    miembros_table.c.nombre,
    miembros_table.c.apellido
).select_from(miembros_table)

def get_members_data(query):
    all_members=[]
    
    with Session() as session:
        results = session.execute(query).fetchall()

        for member in results:
            member_db=Member(**scheme_member_db(member))
            all_members.append(member_db)

    return all_members
