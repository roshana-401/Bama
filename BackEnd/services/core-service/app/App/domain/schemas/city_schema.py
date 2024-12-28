from pydantic import BaseModel,EmailStr,conint,Field
from uuid import UUID

class get_name(BaseModel):
    city_name:str= Field(..., max_length=20,min_length=4)

class get_province_id(BaseModel):
    province_id:UUID
    

class get_city_id(BaseModel):
    city_id:UUID

class city_id(get_city_id):
    pass
class city_info(get_name):
    province_name:str
    pass

class Add_city(get_name,get_province_id):
    pass

class massage(BaseModel):
    massage:str

class massage_city(get_city_id,massage):
    pass
        

class update_city(get_city_id,get_name):
    pass

class city_list(get_city_id,get_name):
    class Config:
        orm_mode = True
        from_attributes = True
