from sqlalchemy import Select,insert
from sqlalchemy.orm import sessionmaker

from db.schemas_tables.schemas_tables import usuario_table

from db.db_session import engine

from extra.schemas_function import scheme_user,scheme_user_db

from entities.user import User_DB,User

from extra.helper_functions import get_update_query,execute_update

Session=sessionmaker(engine)



querry_get_users=(Select(
    usuario_table.c.id_usuario,
    usuario_table.c.user_name,
    usuario_table.c.first_name,
    usuario_table.c.last_name,
    usuario_table.c.email,
    usuario_table.c.category,
    usuario_table.c.phone,
    usuario_table.c.disabled
).select_from(usuario_table)
)

querry_get_users_db=(Select(
    usuario_table.c.id_usuario,
    usuario_table.c.user_name,
    usuario_table.c.password,
    usuario_table.c.first_name,
    usuario_table.c.last_name,
    usuario_table.c.email,
    usuario_table.c.category,
    usuario_table.c.phone,
    usuario_table.c.refresh_token,
    usuario_table.c.disabled
)
)




def update_refresh_token_db(id_user,refresh_token):
    query=get_update_query(table=usuario_table,filters={'id_usuario':id_user},params={'refresh_token':refresh_token})
    execute_update(query=query)


def get_user(user_name:str):
    with Session() as session:
        querry=querry_get_users.where(usuario_table.c.user_name == user_name)
        user_row=session.execute(querry).first()
        
        if not user_row == None:
            print('user row',user_row)
            user_scheme=scheme_user(user_row=user_row)
            user_found=User(**user_scheme)
            
            return user_found
        else:
            return 'User not found'

def get_user_db(user_name:str):
    with Session() as session:
        querry=querry_get_users_db.where(usuario_table.c.user_name == user_name)
        user_row=session.execute(querry).first()
        
        if not user_row == None:
            user_scheme=scheme_user_db(user_row=user_row)
            user_found=User_DB(**user_scheme)
            return user_found
        else:
            return 'User not found'

def get_insert_querry_user(user:User_DB):
    insert_querry=insert(usuario_table).values(
        user_name=user.user_name,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        category=user.category,
        phone=user.phone,
        refresh_token=user.refresh_token,
        disabled=user.disabled
    )
    return insert_querry

def insert_user(user:User_DB):
    querry=get_insert_querry_user(user)

    with Session() as session:
        session.execute(querry)
        session.commit()

    inserted_user=get_user_db(user.user_name)

    return inserted_user

