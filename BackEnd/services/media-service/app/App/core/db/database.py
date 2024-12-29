
from ..config import setting
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = AsyncIOMotorClient(setting.DATABASE_URL)
db = client[setting.DATABASE_NAME]

SQLALCHEMY_DATABASE_URL_USER=f'{setting.DATABASE_DIALECT}://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME_USER}'
engin_user=create_engine(SQLALCHEMY_DATABASE_URL_USER)
SessionLoacalTwo=sessionmaker(autocommit=False,autoflush=False,bind=engin_user)


async def get_db():
    yield db
    
def get_db_user():
    db=SessionLoacalTwo()
    try:
        yield db
    finally:
        db.close()