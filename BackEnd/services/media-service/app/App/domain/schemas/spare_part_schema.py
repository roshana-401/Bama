from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId
from uuid import UUID
    
class GetPictureSpare(BaseModel):
    
    mongo_id:PydanticObjectId

class massageSparePart(BaseModel):
    massage:str

class deletePictureSpare(GetPictureSpare):
    pass


class GetAllMedia(BaseModel):
    sell_spareparts_id:UUID