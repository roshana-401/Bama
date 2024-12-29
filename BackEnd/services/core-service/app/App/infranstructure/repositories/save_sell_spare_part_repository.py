
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import (get_db,get_db_user)
from fastapi import Depends,HTTPException,status
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.save_sell_spare_part import (saveSellSparePart)
from sqlalchemy.dialects.postgresql import UUID

class SaveSellSparePartRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db

    def create_save_sell_spare_part(self,save_sell_spare_part:saveSellSparePart):
        self.db.add(save_sell_spare_part)
        self.db.commit()
        self.db.refresh(save_sell_spare_part)
        return save_sell_spare_part
    
    
    def delete_save_sell_spare_part(self,save_sell_spare_part:saveSellSparePart):
        self.db.delete(save_sell_spare_part)
        self.db.commit()
        
    def find_save_sell_spare_part(self,save_sell_spare_part:saveSellSparePart):
        boolForExist = self.db.query(saveSellSparePart).filter(saveSellSparePart.user_id==save_sell_spare_part.user_id,saveSellSparePart.sell_spare_parts_id==save_sell_spare_part.sell_spare_parts_id)
        if boolForExist.first():
            return True
        else:
            return False
        
    def get_save_sell_spare_part(self,save_sell_spare_part:saveSellSparePart):
        boolForExist = self.db.query(saveSellSparePart).filter(saveSellSparePart.user_id==save_sell_spare_part.user_id,saveSellSparePart.sell_spare_parts_id==save_sell_spare_part.sell_spare_parts_id)
        if not boolForExist.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="این آگهی در لیست مورد علاقه ها وجود ندارد ")
        return boolForExist.first()
        
    def get_all_save_sell_spare_part_by_ID(self,user_id:UUID):
        all_save_spare_part = self.db.query(saveSellSparePart).filter(saveSellSparePart.user_id==user_id)

                                                                                                                    
        return all_save_spare_part.all()
    
    