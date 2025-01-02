from pydantic import BaseModel,EmailStr,conint,Field
from App.domain.models.gearboxStatus import gearboxStatus
from App.domain.models.operation_status import OperationStatus
from datetime import datetime
from uuid import UUID
from typing import Optional
import jdatetime   
current_year = jdatetime.datetime.now().year  

class get_sell_car_id(BaseModel):
    sell_car_id:UUID
    
class get_phone_number(BaseModel):
    phone_number:str
    
class get_description(BaseModel):
    description:str


class update_phone_number(get_phone_number):
    pass

class Add_sell_car_form(BaseModel):
    car_name:str = Field(..., max_length=100,min_length=5,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    model_id:UUID
    price:int=Field(..., ge=5000000)
    color:str= Field(..., max_length=100,min_length=2,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    gearbox: gearboxStatus
    KM:int=Field(..., ge=0)
    Operation:OperationStatus
    year:int=Field(..., ge=1300, le=current_year)
    description:Optional[str]= Field(None, max_length=300,min_length=0,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    city_id:UUID
    
class Add_sell_car(Add_sell_car_form):
    user_id:UUID
    

class sell_car_form(get_phone_number):
    car_name:str
    model_name:str
    price:int
    color:str
    gearbox: gearboxStatus
    KM:int
    Operation:OperationStatus
    year:int
    description:Optional[str]= Field(None, max_length=300,min_length=0,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    city_name:str
    car_compony_name:str
    province_name:str
    dateUpdate:str
    dateCreate:str
    sell_car_id:str
    

class updata_sell_car(get_sell_car_id):
    car_name:Optional[str] = Field(None, max_length=100,min_length=5,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    model_id:Optional[UUID]=None
    price:Optional[int]=Field(None, ge=5000000)
    color:Optional[str]= Field(None, max_length=100,min_length=2,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    gearbox: Optional[gearboxStatus] = None
    KM:Optional[int]=Field(None, ge=0)
    Operation:Optional[OperationStatus]=None
    year:Optional[int]=Field(None, ge=1300, le=current_year)
    description:Optional[str]= Field(None, max_length=300,min_length=0,pattern=r'^[\w\s\-\u0600-\u06FF]+$')
    city_id:Optional[UUID]=None

class filter_data_sell_car(BaseModel):
    model_id:Optional[UUID]=None
    car_compony_id:Optional[UUID]=None
    price_down:Optional[int]=Field(0, ge=0)
    price_top:Optional[int]=Field(float('inf'), ge=0)
    KM_down:Optional[int]=Field(0, ge=0)
    KM_top:Optional[int]=Field(float('inf'), ge=0)
    year:Optional[int]=Field(None, ge=1300, le=current_year)
    gearbox: Optional[gearboxStatus] = None
    car_name:Optional[str]=Field("",pattern=r'^[\w\s\-\u0600-\u06FF]+$')


class massage(BaseModel):
    massage:str

class massage_sell_car(get_sell_car_id,massage):
    pass
        
