from sqlalchemy import select

from db.schemas_tables.schemas_tables import roles_table

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from extra.schemas_function import scheme_role_db

from entities.user import Role

query_get_role=select(roles_table)

Session=sessionmaker(engine)

def get_roles_data(query) -> list[Role]:
    all_roles=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for role in results:
            role_db=Role(**scheme_role_db(role))
            all_roles.append(role_db)
    return all_roles


