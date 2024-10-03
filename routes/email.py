from fastapi import APIRouter,status,HTTPException
from fastapi.responses import JSONResponse
from entities.email import Email,Password_Reset_Request,Password_Reset_Confirm
from db.querries.users import get_user_by_email,update_password
from config.mail import mail,create_message
from config.auth import create_url_safe_token,decode_url_safe_token,hash_password
from config.config import settings
from extra.helper_functions import send_message

email=APIRouter(prefix='/email')

@email.post('/send_mail')
async def send_mail(emails:Email):
    emails=emails.addresses
    html_message="<h1> Welcome to the app </h1>"

    await send_message(subject="Welcome to the web page!",body=html_message,recipients=emails)

    # message=create_message(recipients=emails,
    #                     subject="Welcome",
    #                     body=html)
    
    # await mail.send_message(message=message)

    return {"message":"Email sent successfully"}


@email.post('/password_reset_request')
async def password_reset_request(email_data:Password_Reset_Request):
    
    email=email_data.email

    token=create_url_safe_token(data={"email":email})

    #TODO: MOdificar luego
    link=f"http://{settings.DOMAIN}/email/password_reset_confirm/{token}"

    html_message=f"""

    <h1> Reset your password </h1>
    <p>Please click this link <a href="{link}">link</a> to reset your password</p>

    """

    # message=create_message(recipients=[email],
    #                     subject="Reset your password",
    #                     body=html_message)
    
    # await mail.send_message(message=message)

    await send_message(subject="Reset your password",body=html_message,recipients=[email])

    return JSONResponse(
        content={"message":"Please check your email for intructions to reset your password"},
        status_code=status.HTTP_200_OK
    )

@email.post('/password_reset_confirm/{token}')
async def password_reset_confirm(token:str,passwords:Password_Reset_Confirm):

    if passwords.new_password !=passwords.confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Passwords do not match')

    token_data=decode_url_safe_token(token)
    user_email=token_data.get('email')

    if user_email:
        user=get_user_by_email(email=user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Email not found")
        password_hash=hash_password(password=passwords.new_password)
        update_password(id_user=user.id,password=password_hash)
        return JSONResponse(
            content={"message":"Password reset successfully"},
            status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"message":"Error occured during the process"}
        )
    

