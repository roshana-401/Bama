from pydantic import BaseModel,EmailStr,conint,Field
from App.domain.models.operation_status import OperationStatus
from uuid import UUID
from typing import Optional
import jdatetime  
 
current_year = jdatetime.datetime.now().year  

class get_sell_spare_part_id(BaseModel):
    sell_spare_part_id:UUID
    
class get_phone_number(BaseModel):
    phone_number:str
    
class get_description(BaseModel):
    description:str


class update_phone_number(get_phone_number):
    pass

class Add_sell_spare_part_form(BaseModel):
    spare_part_name:str = Field(..., max_length=100,min_length=5,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    model_id:UUID
    price:int=Field(..., ge=5000000)
    Operation:OperationStatus
    description:Optional[str]= Field(None, max_length=300,min_length=0,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    city_id:UUID
    
class Add_sell_spare_part(Add_sell_spare_part_form):
    user_id:UUID
    

class sell_spare_part_form(get_phone_number):
    spare_part_name:str
    model_name:str
    price:int
    Operation:OperationStatus
    description:Optional[str]= Field(None, max_length=300,min_length=0,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    city_name:str
    car_compony_name:str
    province_name:str
    dateUpdate:str
    dateCreate:str
    sell_spare_part_id:str
    

class updata_sell_spare_part(get_sell_spare_part_id):
    spare_part_name:Optional[str] = Field(None, max_length=100,min_length=5,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    model_id:Optional[UUID]=None
    price:Optional[int]=Field(None, ge=5000000)
    Operation:Optional[OperationStatus]=None
    description:Optional[str]= Field(None, max_length=300,min_length=0,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    city_id:Optional[UUID]=None

class filter_data_sell_spare_part(BaseModel):
    model_id:Optional[UUID]=None
    car_compony_id:Optional[UUID]=None
    price_down:Optional[int]=Field(0, ge=0)
    price_top:Optional[int]=Field(float('inf'), ge=0)
    spare_part_name:Optional[str]=Field("",pattern=r'^[\w\s\-\u0600-\u06FF]+$')


class massage(BaseModel):
    massage:str

class massage_sell_spare_part(get_sell_spare_part_id,massage):
    pass
        
