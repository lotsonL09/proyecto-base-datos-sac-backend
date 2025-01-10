from fastapi import Depends,HTTPException,status

from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from config.config import settings

import jwt

from jwt import InvalidTokenError

from datetime import datetime,timedelta,timezone

from entities.user import User,User_DB

from db.querries.users import get_user,get_user_db,insert_user

from extra.helper_functions import get_update_query,execute_update

from db.schemas_tables.schemas_tables import usuario_table

from config.config import settings

from config.mail import create_url_safe_token, decode_url_safe_token,create_message,mail

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')

"""
Para la encriptacion con jwt
"""
ALGORITHM=settings.ALGORITHM
ACCESS_TOKEN_DURATION=settings.ACCESS_TOKEN_EXPIRE_MINUTES 
SECRET_KEY=settings.SECRET_KEY #openssl rand -hex 32


"""
Contexto de encriptacion: el schema define el algoritmo de hash que se va a usar.
"""

pwd_context=CryptContext(schemes=['bcrypt'])


def create_access_token(subject:str,id_role:int,expire_delta:int = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    expire=datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload={
        "sub":subject,
        "exp":expire,
        "role":id_role,
        "mode":"access_token"
    }
    token=jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def create_refresh_token(subject:str,id_role:int,expire_delta:int=settings.REFRESH_TOKEN_EXPIRE_MINUTES):
    expire=datetime.now(timezone.utc) + timedelta(minutes=expire_delta)
    payload={
        "sub":subject,
        "exp":expire,
        "role":id_role,
        "mode":"refresh_token"
    }
    token=jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token

def update_refresh_token_db(id_user,refresh_token):
    query=get_update_query(table=usuario_table,filters={'id_usuario':id_user},params={'refresh_token':refresh_token})
    execute_update(query=query)

error=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials',
            headers={"www-Authenticate":"Bearer"}
        )

async def auth_user(token:dict=Depends(oauth2_scheme)) -> User | str:
    #Validate the refresh jwt token 
    try:
        data=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if ('user_name' not in data) and ('mode' not in data):
            raise error
        if data['mode'] != 'access_token':
            raise error
        user_name=data.get("sub")
        if user_name is None:
            raise error
        #return get_user(user_name=user_name)
        return get_user(field="user_name",value=user_name)
    except InvalidTokenError:
        raise error

async def refresh_token(token:str=Depends(oauth2_scheme)):
    try:
        data=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if ('user_name' not in data) and ('mode' not in data):
            raise error
        if data['mode'] != 'refresh_token':
            raise error
        user_name=data.get('sub')
        user=get_user_db(user_name=user_name)
        if (type(user) != User_DB) or (token != user.refresh_token):
            raise error
        
        #generate new refresh token and update user
        refresh_token=create_refresh_token(subject=user_name)
        update_refresh_token_db(id_user=user.id,refresh_token=refresh_token)
        access_token=create_access_token(subject=user_name)

        return {
            'access_token':access_token,
            'refresh_token':refresh_token,
            "token_type":"bearer"
        }
    except InvalidTokenError:
        error

def login_process(user_form,password_form):
    user=get_user_db(user_form)

    if not type(user) == User_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='The user name is wrong'
        )
    
    if not pwd_context.verify(password_form,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='The password is wrong'
        )
    
    access_token=create_access_token(subject=user.user_name,id_role=user.role.id)

    refresh_token=create_refresh_token(subject=user.user_name,id_role=user.role.id)

    #store the refresh token in memory | database | any storage
    update_refresh_token_db(id_user=user.id,refresh_token=refresh_token)

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }

def hash_password(password:str):
    return pwd_context.hash(password)

async def register_process(user:User_DB,collection:str):

    if type(get_user(field="user_name",value=user.user_name)) == User:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail='User already exists')
    
    if type(get_user(field="email",value=user.email)) == User:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail='Email already exists')
    
    pwd_encrypted=pwd_context.hash(user.password)
    user.password=pwd_encrypted

    user_data=insert_user(user=user,collection=collection)

    token=create_url_safe_token(data={"email":user.email})

    #TODO: MOdificar luego
    link=f"http://{settings.DOMAIN}/login/verify/{token}"

    html_message=f"""

    <h1> Verify your Email </h1>
    <p>Please click this link <a href="{link}">link</a> to verify your email</p>


    """

    message=create_message(recipients=[user.email],
                        subject="Verify your email",
                        body=html_message)
    
    await mail.send_message(message=message)

    return {
        "detail":"Account created! Check email to verify your account",
        "user_data":user_data
    }


