from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId
from uuid import UUID
    
class GetPictureCar(BaseModel):
    
    mongo_id:PydanticObjectId

class deletePictureCar(GetPictureCar):
    pass


class massageCar(BaseModel):
    massage:str

class GetAllMedia(BaseModel):
    sell_car_id:UUID