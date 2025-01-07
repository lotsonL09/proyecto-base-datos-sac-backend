from sqlalchemy import create_engine,URL
from config.config import settings

db_config = {
    "drivername":settings.DRIVER_NAME,
    "username":settings.USERNAME,
    "password":settings.PASSWORD,
    "host":settings.HOST,
    "port":settings.PORT,
    "database":settings.DATABASE
}

url_db=URL.create(**db_config)

engine=create_engine(url_db)