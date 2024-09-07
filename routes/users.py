from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.responses import JSONResponse
from db.querries.users import get_user,get_user_by_id

from entities.user import User

from config.auth import auth_user

users=APIRouter(prefix='/users',
                tags=['Users site'],
                responses={status.HTTP_404_NOT_FOUND:{"message":"Page not found"}})

async def get_current_user(user:User=Depends(auth_user)):
    user=get_user(user_name=user.user_name)
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Inactive user',
                            headers={"www-Authenticate":"Bearer"})
    return user

@users.get('/me')
async def return_user_me(current_user:User=Depends(get_current_user)):
    return current_user

@users.get('/{id}')
async def return_user(id:int):

    user=get_user_by_id(id=id)

    return user