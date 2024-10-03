from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from config.config import settings
from fastapi import HTTPException,status

from itsdangerous import URLSafeTimedSerializer

mail_config=ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

mail=FastMail(
    config=mail_config
)

def create_message(recipients:list[str],subject:str,body:str):
    message=MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
    
    return message

serializer=URLSafeTimedSerializer(
        secret_key=settings.SECRET_KEY,
        salt="email-configuration"
    )

def create_url_safe_token(data:dict):
    
    token=serializer.dumps(obj=data)
    
    return token

def decode_url_safe_token(token:str):
    try:
        token_data=serializer.loads(token)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
