
from pymongo.collection import Collection
from App.domain.models.MediaModel import (
    MediaModelCar,MediaModelSpareParts,MediaModelToMongoCar,MediaModelToMongoSpare
)
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient
)
from typing import Annotated
from fastapi import Depends,HTTPException,status
from App.core.db.database import get_db

class MediaRepositoryCar:
    def __init__(self,db: Annotated[AsyncIOMotorClient, Depends(get_db)]) -> None:
        
        self.collectionCar=db["CarMedia"]
        
    async def create_car(self,media_car:MediaModelToMongoCar):
        save_file=await self.collectionCar.insert_one(media_car.dict())
        mongo_id=save_file.inserted_id
        return mongo_id
    
    async def get_all_car(self,car_sell_id:str):
        cars =await self.collectionCar.find({"sell_car_id": car_sell_id}) 
        car=[MediaModelCar(**car) for car in cars]
        print(car)
        return [MediaModelCar(**car) for car in cars]
    
    async def get_car(self,mongo_id:ObjectId):
        print("get carssss")
        car =await self.collectionCar.find_one({"_id": mongo_id}) 
        if car is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="رسانه مورد نظر یافت نشد")
        return MediaModelCar(
                mongo_id=car["_id"],
                storage_id=car["storage_id"],
                filename=car["filename"],
                content_type=car["content_type"],
                size=car["size"],
                user_id=car["user_id"],
                sell_car_id=car["sell_car_id"]
        )
    
class MediaRepositorySpareParts:
    def __init__(self,db: Annotated[AsyncIOMotorClient, Depends(get_db)]) -> None:
        
        self.collectionSpareParts=db["SpareParts"]
        
    async def create_sparePart(self,media_spare:MediaModelToMongoSpare):
        save_file=await self.collectionSpareParts.insert_one(media_spare.dict())
        mongo_id=save_file.inserted_id
        return mongo_id
    
    async def get_all_sparePart(self,sell_spareparts_id:str):
        spareParts =await self.collectionSpareParts.find({"sell_spareparts_id": sell_spareparts_id}) 
        sparePart=[MediaModelSpareParts(**sparePart) for car in spareParts]
        print(sparePart)
        return [MediaModelCar(**sparePart) for sparePart in spareParts]
    
    async def get_sparePart(self,mongo_id:ObjectId):
        sparePart =await self.collectionSpareParts.find_one({"_id": mongo_id}) 
        if sparePart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="رسانه مورد نظر یافت نشد")
        return MediaModelSpareParts(
            mongo_id=sparePart["_id"],
            storage_id=sparePart["storage_id"],
            filename=sparePart["filename"],
            content_type=sparePart["content_type"],
            size=sparePart["size"],
            user_id=sparePart["user_id"],
            sell_spareparts_id=sparePart["sell_spareparts_id"]
        )