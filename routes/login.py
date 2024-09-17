from fastapi import APIRouter,status,HTTPException,Depends

from fastapi.security import OAuth2PasswordRequestForm

from entities.user import User_DB,User

from db.querries.users import get_user

from config.auth import auth_user,refresh_token,login_process,register_process

login=APIRouter(prefix='/login',
                tags=['Login site'],
                responses={status.HTTP_404_NOT_FOUND:{'message':'Page not found'}})

@login.post('/')
async def login_root(form:OAuth2PasswordRequestForm=Depends()):
    print("formulario: ",form.username)
    return login_process(user_form=form.username,password_form=form.password)

@login.post('/register')
async def register_user(user:User_DB)->User:
    
    return register_process(user=user)

@login.post('/refresh_token')
async def get_refresh_token(info_user_token:str=Depends(refresh_token)):
    return info_user_token

