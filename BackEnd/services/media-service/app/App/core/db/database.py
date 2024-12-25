
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ..config import setting
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(setting.DATABASE_URL)
db = client[setting.DATABASE_NAME]
async def get_db():
    yield db