from fastapi import UploadFile,Depends
from pymongo.database import Database
from motor.motor_asyncio import (
    AsyncIOMotorGridFSBucket,
    AsyncIOMotorClient
)
from typing import Annotated

from bson import ObjectId
from App.core.db.database import get_db



class GridFsStorageForCar:
    def __init__(self,db: Annotated[AsyncIOMotorClient, Depends(get_db)]) -> None:
        self.db=db
        self.gridFs=None
    
    async def init_fs(self):
        if self.gridFs is None:
            self.gridFs=AsyncIOMotorGridFSBucket(self.db,bucket_name="carGridFs")#GridFS production
    
    async def save_file(self,file:UploadFile):
        print("saving")
        await self.init_fs()
        grid=self.gridFs.open_upload_stream(
            filename=file.filename,
            metadata={"content_type":file.content_type},
            
        )
        await grid.write(await file.read())
        await grid.close()
        print("save")
        return grid._id
    
    async def get_file(self,grid_id:ObjectId):
        await self.init_fs()
        file_object=await self.gridFs.open_download_stream(file_id=grid_id)
        return await file_object.read()
    
    async def delete_file(self,grid_id:ObjectId):
        await self.init_fs()
        await self.gridFs.delete(grid_id)
        return {"massage":"رسانه با موفقیت حذف شد"}
    
class GridFsStorageForSpareParts:
    def __init__(self,db: Annotated[AsyncIOMotorClient, Depends(get_db)]) -> None:
        self.db=db
        self.gridFs=None
    
    async def init_fs(self):
        if self.gridFs is None:
            self.gridFs=AsyncIOMotorGridFSBucket(self.db,bucket_name="SparePartsGridFs")#GridFS production
    
    async def save_file(self,file:UploadFile):
        await self.init_fs()
        grid=self.gridFs.open_upload_stream(
            filename=file.filename,
            metadata={"content_type":file.content_type}
        )
        await grid.write(await file.read())
        await grid.close()
        return grid._id
    
    async def get_file(self,grid_id:ObjectId):
        await self.init_fs()
        file_object=await self.gridFs.open_download_stream(file_id=grid_id)
        
        return await file_object.read()
    
    async def delete_file(self,grid_id:ObjectId):
        await self.init_fs()
        await self.gridFs.delete(file_id=grid_id)
        return {"massage":"رسانه با موفقیت حذف شد"}
    
    