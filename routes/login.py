from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext

from entities.user import User_DB,User

from db.querries.users import get_user,get_user_db,insert_user

import jwt

from jwt.exceptions import InvalidTokenError

from datetime import datetime,timedelta,timezone

from extra.helper_functions import create_access_token,create_refresh_access_token

login=APIRouter(prefix='/login',
                tags=['Login site'],
                responses={status.HTTP_404_NOT_FOUND:{'message':'Page not found'}})

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')



#Algoritmo de encriptacion
"""
Para la encriptacion con jwt
"""
ALGORITHM='HS256'
ACCESS_TOKEN_DURATION=10 #min
SECRET_KEY='41afb88eaadf2d1b57ac6cb3cedc5f24b15f5855ffbec6eb33ae355581e23003' #openssl rand -hex 32


"""
Contexto de encriptacion: el schema define el algoritmo de hash que se va a usar.
"""

pwd_context=CryptContext(schemes=['bcrypt'])


@login.post('/')
async def login_root(form:OAuth2PasswordRequestForm=Depends()):

    user=get_user_db(form.username)

    if not type(user) == User_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='The user name is wrong'
        )
    
    if not pwd_context.verify(form.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='The password is wrong'
        )
    
    access_token=create_access_token(subject=user.user_name)

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }


@login.post('/register')
async def register_user(user:User_DB)->User:

    if type(get_user(user.user_name)) == User:
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail='User already exists')
    
    pwd_encrypted=pwd_context.hash(user.password)
    user.password=pwd_encrypted

    user_data=insert_user(user=user)

    return user_data


async def auth_user(token:str=Depends(oauth2_scheme)) -> User | str:
    exception=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials',
            headers={"www-Authenticate":"Bearer"}
        )
    try:
        user_name=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]).get("sub")
        if user_name is None:
            raise exception
        return get_user(user_name=user_name)
    except InvalidTokenError:
        raise exception


async def get_current_user(user:User=Depends(auth_user)):
    user=get_user(user_name=user.user_name)
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Inactive user',
                            headers={"www-Authenticate":"Bearer"})
    return user

@login.get('/users/me')
async def me(current_user:User=Depends(get_current_user)):
    return current_user