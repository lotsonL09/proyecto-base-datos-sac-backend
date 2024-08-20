from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from passlib.context import CryptContext


from entities.user import User_DB,User

from db.querries.users import get_user,get_user_db,insert_user

login=APIRouter(prefix='/login',
                tags=['Login site'],
                responses={status.HTTP_404_NOT_FOUND:{'message':'Page not found'}})

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

pwd_context=CryptContext(schemes=['bcrypt'])

# secret='59c38e4849250ebca7e984ca1b2c1dfdf02f35257a4f6eff35c23728f79cc4da'
# algorithm='HS256'

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
    
    return {
        "access_token":user.user_name,
        "token_type":"bearer"
    }


@login.post('/register')
async def register_user(user:User_DB)->User:

    #funcion for search user

    if type(get_user(user.user_name)) == User:
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail='User already exists')
    
    pwd_encrypted=pwd_context.hash(user.password)
    user.password=pwd_encrypted

    user_data=insert_user(user=user)

    return user_data

async def get_current_user(token:str=Depends(oauth2_scheme)):
    user_name=token
    user=get_user(user_name=user_name)

    if not type(user) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials',
            headers={"www-Authenticate":"Bearer"}
        )
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Inactive user',
                            headers={"www-Authenticate":"Bearer"})

    return user

@login.get('/users/me')
async def me(
    current_user:User=Depends(get_current_user)
):
    print('0')
    return current_user