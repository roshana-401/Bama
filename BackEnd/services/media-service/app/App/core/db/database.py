
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ..config import setting
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["BamaMediaDB"]
async def get_db():
    yield db