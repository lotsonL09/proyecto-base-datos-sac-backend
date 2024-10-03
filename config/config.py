from pydantic_settings import BaseSettings
from pydantic import NonNegativeInt
from pathlib import Path

"""
BaseSettings: Es una clase de Pydantic que se utiliza para manejar configuraciones.

Permite cargar variables desde un archivo '.env'
"""

class Settings(BaseSettings):

    #database related
    DRIVER_NAME:str
    USERNAME:str
    PASSWORD:str
    HOST:str
    PORT:NonNegativeInt
    DATABASE:str

    #JWT Token related
    SECRET_KEY:str
    REFRESH_SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_MINUTES:int

    #email

    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM_NAME:str
    MAIL_STARTTLS:bool = True
    MAIL_SSL_TLS:bool = False
    USE_CREDENTIALS:bool = True
    VALIDATE_CERTS:bool = True

    DOMAIN:str


    class Config:
        env_file= ".env"

settings=Settings()


