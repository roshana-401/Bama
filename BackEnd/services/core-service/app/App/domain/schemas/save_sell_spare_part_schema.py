from pydantic import BaseModel,EmailStr,conint,Field
from uuid import UUID
from typing import Optional
 

class get_sell_spare_part_id(BaseModel):
    sell_spare_part_id:UUID
    
class get_user_id(BaseModel):
    user_id:UUID

class get_user_id_For_save(BaseModel):
    user_id:Optional[UUID]=None

class all_save_sell_spare_part(get_sell_spare_part_id):
    pass
class save_sell_spare_part(get_sell_spare_part_id):
    user_id:Optional[UUID]=None

class massage(BaseModel):
    massage:str