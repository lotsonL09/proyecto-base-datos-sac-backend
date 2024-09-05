from fastapi import APIRouter,status,HTTPException,Depends

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext

from entities.user import User_DB,User

from db.querries.users import get_user,get_user_db,insert_user,update_refresh_token_db

import jwt

from jwt.exceptions import InvalidTokenError

from extra.helper_functions import create_access_token,create_refresh_token

from config.config import settings

login=APIRouter(prefix='/login',
                tags=['Login site'],
                responses={status.HTTP_404_NOT_FOUND:{'message':'Page not found'}})

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')  #lo que valla al endpoint /login



#Algoritmo de encriptacion
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


@login.post('/')
async def login_root(form:OAuth2PasswordRequestForm=Depends()):

    user=get_user_db(form.username)

    print('User',user)

    if not type(user) == User_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='The user name is wrong'
        )
    
    if not pwd_context.verify(form.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail='The password is wrong'
        )
    
    access_token=create_access_token(subject=user.user_name)

    refresh_token=create_refresh_token(subject=user.user_name)

    #store the refresh token in memory | database | any storage
    update_refresh_token_db(id_user=user.id,refresh_token=refresh_token)

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
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



async def refresh_token(token:str=Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
        headers={'www-Authenticate':"Bearer"}
    )

    try:
        data=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if ('user_name' not in data) and ('mode' not in data):
            raise exception
        if data['mode'] != 'refresh_token':
            raise exception
        user_name=data.get('sub')
        print(f'user_name: {user_name}')
        user=get_user_db(user_name=user_name)
        print(f'User class: {user}')
        if (type(user) != User_DB) or (token != user.refresh_token):
            raise exception
        
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
        pass

    return

async def auth_user(token:dict=Depends(oauth2_scheme)) -> User | str:
    exception=HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials',
            headers={"www-Authenticate":"Bearer"}
        )
    #Validate the refresh jwt token 
    try:
        data=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if ('user_name' not in data) and ('mode' not in data):
            raise exception
        if data['mode'] != 'access_token':
            raise exception
        user_name=data.get("sub")
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

@login.post('/refresh_token')
async def get_refresh_token(info_user_token:str=Depends(refresh_token)):
    return info_user_token

