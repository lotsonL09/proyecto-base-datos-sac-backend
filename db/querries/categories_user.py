from sqlalchemy import select

from db.schemas_tables.schemas_tables import categories_user_table

from sqlalchemy.orm import sessionmaker

from db.db_session import engine

from extra.schemas_function import scheme_category_user_db

from entities.user import Category

query_get_category=select(categories_user_table)

Session=sessionmaker(engine)

def get_categories_data(query) -> list[Category]:
    all_categories=[]
    with Session() as session:
        results=session.execute(query).fetchall()
        for categoriy in results:
            categoriy_db=Category(**scheme_category_user_db(categoriy))
            all_categories.append(categoriy_db)
    return all_categories


