from pydantic import BaseModel,EmailStr,conint,Field
from uuid import UUID

class get_name(BaseModel):
    province_name:str= Field(..., max_length=20,min_length=4,pattern=r'^[\w\s\-\u0600-\u06FF]+$')

class get_province_id(BaseModel):
    province_id:UUID

class Add_province(get_name):
    pass
    
class update_province_name(get_name):
    pass

class province_id(get_province_id):
    pass

class massage(BaseModel):
    massage:str

class massage_province(get_province_id,massage):
    pass
        

class update_province(get_province_id,get_name):
    pass

class province_list(get_province_id,get_name):
    class Config:
        orm_mode = True
        from_attributes = True
