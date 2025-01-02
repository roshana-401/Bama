from pydantic import BaseModel,EmailStr,conint,Field
from uuid import UUID

class get_name(BaseModel):
    model_car_name:str= Field(..., max_length=20,min_length=4,pattern=r'^[\w\s\-\u0600-\u06FF]+$')

class get_car_compony_id(BaseModel):
    car_compony_id:UUID
    

class get_model_car_id(BaseModel):
    model_id:UUID

class model_car_id(get_model_car_id):
    pass
class model_car_info(get_name):
    car_compony_name:str
    

class Add_model_car(get_name,get_car_compony_id):
    pass

class massage(BaseModel):
    massage:str

class massage_model_car(get_model_car_id,massage):
    pass
        

class update_model_car(get_model_car_id,get_name):
    pass

class model_car_list(get_model_car_id,get_name):
    class Config:
        orm_mode = True
        from_attributes = True
