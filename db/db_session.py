from sqlalchemy import create_engine

url_db="mysql+pymysql://root:1234@localhost:3306/sac"   #para william

engine=create_engine(url_db)