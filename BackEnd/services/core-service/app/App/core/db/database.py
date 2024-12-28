from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import setting

SQLALCHEMY_DATABASE_URL=f'{setting.database_dialect}://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'
SQLALCHEMY_DATABASE_URL_USER=f'{setting.database_dialect}://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name_user}'

engin=create_engine(SQLALCHEMY_DATABASE_URL)
engin_user=create_engine(SQLALCHEMY_DATABASE_URL_USER)

SessionLoacal=sessionmaker(autocommit=False,autoflush=False,bind=engin)
SessionLoacalTwo=sessionmaker(autocommit=False,autoflush=False,bind=engin_user)

Base=declarative_base()

def get_Base_Class():
    return Base

def get_db():
    db=SessionLoacal()
    try:
        yield db
    finally:
        db.close()
        
def get_db_user():
    db=SessionLoacalTwo()
    try:
        yield db
    finally:
        db.close()