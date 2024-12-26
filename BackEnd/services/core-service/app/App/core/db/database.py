from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import setting

SQLALCHEMY_DATABASE_URL=f'{setting.database_dialect}://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

engin=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLoacal=sessionmaker(autocommit=False,autoflush=False,bind=engin)

Base=declarative_base()

def get_Base_Class():
    return Base
def get_db():
    db=SessionLoacal()
    try:
        yield db
    finally:
        db.close()