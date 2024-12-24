


from pydantic import BaseModel,EmailStr,conint,Field
from datetime import datetime
from uuid import UUID

class MediaResponse(BaseModel):
    mongo_id:str
    filename:str
    size:str
    massage:str