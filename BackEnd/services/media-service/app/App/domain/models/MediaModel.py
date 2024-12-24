
from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId



class MediaModelToMongo(BaseModel):
    filename: str
    storage_id:PydanticObjectId
    content_type: str
    size: str
    user_id: str

class MediaModelToMongoCar(MediaModelToMongo):
    sell_car_id:str

class MediaModelToMongoSpare(MediaModelToMongo):
    sell_spareparts_id:str
    
    
    
    

class MediaModel(BaseModel):
    mongo_id: PydanticObjectId=None
    filename: str
    content_type: str
    size: str
    user_id: str


class MediaGridFs(MediaModel):
    storage_id:PydanticObjectId
    
class MediaModelCar(MediaGridFs):
    sell_car_id:str

class MediaModelSpareParts(MediaGridFs):
    sell_spareparts_id:str