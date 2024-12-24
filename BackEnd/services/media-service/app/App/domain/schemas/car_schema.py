from pydantic import BaseModel
from pydantic_mongo import PydanticObjectId

    
class GetPictureCar(BaseModel):
    
    mongo_id:PydanticObjectId

