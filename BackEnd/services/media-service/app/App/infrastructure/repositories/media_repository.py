
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
    
    async def get_all_car(self,car_sell_id:str,user_id:str):
        cars_cursor = self.collectionCar.find({"sell_car_id": car_sell_id}) 
        cars = await cars_cursor.to_list(None)
        if not cars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="هیچ رسانه‌ای پیدا نشد.")
        all_media=[]
        for car in cars:
            if car["user_id"]==user_id:
                all_media.append({"media_id": str(car["_id"])})
        all_media.append({"number Of Picture":len(all_media)})
        return all_media
    
    async def get_car(self,mongo_id:ObjectId):
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
    async def delete_car(self,mongo_id:ObjectId,user_id:str):
        car =await self.collectionCar.find_one({"_id": mongo_id}) 
        if car is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="رسانه مورد نظر یافت نشد")
        if car["user_id"]!=user_id:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="کاربر اجازه دسترسی به این رسانه را ندارد",
                    )
        await self.collectionCar.delete_one({"_id": mongo_id})
    
class MediaRepositorySpareParts:
    def __init__(self,db: Annotated[AsyncIOMotorClient, Depends(get_db)]) -> None:
        
        self.collectionSpareParts=db["SpareParts"]
        
    async def create_sparePart(self,media_spare:MediaModelToMongoSpare):
        save_file=await self.collectionSpareParts.insert_one(media_spare.dict())
        mongo_id=save_file.inserted_id
        return mongo_id
    
    async def get_all_spareParts(self,sell_spareparts_id:str,user_id:str):
        spareParts_cursor = self.collectionSpareParts.find({"sell_spareparts_id": sell_spareparts_id}) 
        spareparts = await spareParts_cursor.to_list(None)
        if not spareparts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="هیچ رسانه‌ای پیدا نشد.")
        all_media=[]
        for sparepart in spareparts:
            if sparepart["user_id"]==user_id:
                all_media.append({"media_id": str(sparepart["_id"])})
        all_media.append({"number Of Picture":len(all_media)})
        return all_media
    
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
    async def delete_sparePart(self,mongo_id:ObjectId,user_id:str):
        sparePart =await self.collectionSpareParts.find_one({"_id": mongo_id}) 
        if sparePart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="رسانه مورد نظر یافت نشد")
        if sparePart["user_id"]!=user_id:
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="کاربر اجازه دسترسی به این رسانه را ندارد",
                    )
        await self.collectionSpareParts.delete_one({"_id": mongo_id})