from pydantic import BaseModel,EmailStr,conint,Field
from uuid import UUID

class get_name(BaseModel):
    car_compony_name:str= Field(..., max_length=20,min_length=4,pattern=r'^[\w\s\-\u0600-\u06FF]+$')

class get_car_compony_id(BaseModel):
    car_compony_id:UUID

class Add_car_compony(get_name):
    pass
    
class update_car_compony_name(get_name):
    pass

class compony_car_id(get_car_compony_id):
    pass

class massage(BaseModel):
    massage:str

class massage_car_compony(get_car_compony_id,massage):
    pass
        

class update_car_compony(get_car_compony_id,get_name):
    pass

class car_compony_list(get_car_compony_id,get_name):
    class Config:
        orm_mode = True
        from_attributes = True
