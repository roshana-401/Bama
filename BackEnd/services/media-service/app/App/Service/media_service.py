
from typing import Annotated,List
from App.infrastructure.repositories.media_repository import (MediaRepositoryCar,MediaRepositorySpareParts)
from fastapi import Depends, UploadFile, HTTPException, status
from App.infrastructure.storage.gridFs_storage import (GridFsStorageForCar,GridFsStorageForSpareParts)
from bson import ObjectId
from App.domain.models.MediaModel import (
    MediaModelCar,
    MediaModelToMongoCar,
    MediaModelToMongoSpare,
    MediaModel,
    MediaGridFs,
    MediaModelSpareParts
)
import base64
from fastapi.responses import StreamingResponse
from io import BytesIO
from App.domain.schemas.Media_schema import MediaResponse

class MediaServiceCar:
    
    def __init__(self
                 ,media_response:Annotated[MediaRepositoryCar,Depends()],
                 storage:Annotated[GridFsStorageForCar,Depends()]):
        self.media_response=media_response
        self.storage=storage
        
    async def create_media_car(self, file: UploadFile, user_id: str,car_sell_id:str):
        storage_id=await self.storage.save_file(file=file)
        media_car=MediaModelToMongoCar(
            content_type=file.content_type,
            storage_id=storage_id,
            filename=file.filename,
            size=str(file.size),
            user_id=user_id,
            sell_car_id=car_sell_id
        )
        mongo_id=await self.media_response.create_car(media_car=media_car)
        
        return MediaResponse(
            mongo_id=str(mongo_id),
            filename=file.filename,
            size=str(file.size),
            massage="رسانه با موفیت ذخیره شد"
        )
       
    async def get_all_madia_car(self,car_sell_id:str,user_id:str):
        return await self.media_response.get_all_car(car_sell_id,user_id)
                
    async def media_car(self,mongo_id:ObjectId,user_id:str):
        media=await self.media_response.get_car(mongo_id)
        
        if media.user_id!=user_id:
                 raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="کاربر اجازه دسترسی به این رسانه را ندارد",
                    )
        file=await  self.storage.get_file(media.storage_id)
        return file ,media
       
    async def get_madia_car(self,mongo_id:ObjectId,user_id:str):
        file , media=await self.media_car(mongo_id,user_id)
        def file_stream():
            yield file
                
        return [
                    MediaModel(
                        mongo_id=media.mongo_id,
                        content_type=media.content_type,
                        filename=media.filename,
                        size=media.size,
                        user_id=user_id    
                    ),
                    file_stream
        ]      
        
    async def delete_madia_car(self,mongo_id:ObjectId,user_id:str):
        media=await self.media_response.get_car(mongo_id)
        await self.media_response.delete_car(mongo_id,user_id)
        return await self.storage.delete_file(media.storage_id)
        
                
        
class MediaServiceSpareParts:
    
    def __init__(self
                 ,media_response:Annotated[MediaRepositorySpareParts,Depends()],
                 storage:Annotated[GridFsStorageForSpareParts,Depends()]):
        self.media_response=media_response
        self.storage=storage
        
    async def create_media_sparePart(self, file: UploadFile, user_id: str,sell_spareparts_id:str):
        storage_id=await self.storage.save_file(file=file)
        media_sparePart=MediaModelToMongoSpare(
            content_type=file.content_type,
            storage_id=storage_id,
            filename=file.filename,
            size=str(file.size),
            user_id=user_id,
            sell_spareparts_id=sell_spareparts_id
        )
        mongo_id=await self.media_response.create_sparePart(media_spare=media_sparePart)
        
        return MediaResponse(
            mongo_id=str(mongo_id),
            filename=file.filename,
            size=str(file.size),
            massage="رسانه با موفیت ذخیره شد"
        )
        
    async def delete_madia_sparePart(self,mongo_id:ObjectId,user_id:str):
        media=await self.media_response.get_sparePart(mongo_id)
        await self.media_response.delete_sparePart(mongo_id,user_id)
        return await self.storage.delete_file(media.storage_id)
     
        
    async def media_sparePart(self,mongo_id:ObjectId,user_id:str):
        media=await self.media_response.get_sparePart(mongo_id)
        if media.user_id!=user_id:
                 raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="کاربر اجازه دسترسی به این رسانه را ندارد",
        )
        
        file=await self.storage.get_file(media.storage_id)
        return file,media
    async def get_all_madia_spareParts(self,sell_spareparts_id:str,user_id:str):
        return await self.media_response.get_all_spareParts(sell_spareparts_id,user_id)   
    async def get_madia_sparePart(self,mongo_id:ObjectId,user_id:str):
            file,media=await self.media_sparePart(mongo_id,user_id)
            
            def file_stream():
                yield file
                
            return [
                    MediaModel(
                        mongo_id=media.mongo_id,
                        content_type=media.content_type,
                        filename=media.filename,
                        size=media.size,
                        user_id=user_id    
                    ),
                    file_stream
            ]        
        
