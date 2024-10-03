from fastapi import APIRouter,status,HTTPException,Depends

from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import JSONResponse

from entities.user import User_DB

from db.querries.users import get_user_by_email

from config.auth import auth_user,refresh_token,login_process,register_process

from config.mail import decode_url_safe_token

login=APIRouter(prefix='/login',
                tags=['Login site'],
                responses={status.HTTP_404_NOT_FOUND:{'message':'Page not found'}})

@login.post('/')
async def login_root(form:OAuth2PasswordRequestForm=Depends()):
    return login_process(user_form=form.username,password_form=form.password)

@login.post('/register')
async def register_user(user:User_DB): 
    return await register_process(user=user)

@login.post('/refresh_token')
async def get_refresh_token(info_user_token:str=Depends(refresh_token)):
    return info_user_token

@login.get('/verify/{token}')
async def verify_user_account(token:str):
    token_data=decode_url_safe_token(token)
    user_email=token_data.get('email')

    if user_email:
        user=get_user_by_email(email=user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        return JSONResponse(
            content={"message":"Account verified successfully"},
            status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message":"Error occured during verification"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )