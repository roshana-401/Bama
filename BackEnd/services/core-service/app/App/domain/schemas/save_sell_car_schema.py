from pydantic import BaseModel,EmailStr,conint,Field
from uuid import UUID
from typing import Optional
 

class get_sell_car_id(BaseModel):
    sell_car_id:UUID
    
class get_user_id(BaseModel):
    user_id:UUID

class all_save_sell_car(get_sell_car_id):
    pass
class save_sell_car(get_sell_car_id):
    user_id:Optional[UUID]=None

class massage(BaseModel):
    massage:str