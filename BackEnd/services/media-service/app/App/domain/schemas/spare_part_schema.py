from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId

    
class GetPictureSpare(BaseModel):
    
    mongo_id:PydanticObjectId

