from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db
from fastapi import Depends,HTTPException,status
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.sell_spare_part import spareParts
import json

class SparePartRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db
        
        
    def create_spare_part(self,sparepart:spareParts):
        self.db.add(sparepart)
        self.db.commit()
        self.db.refresh(sparepart)
        return sparepart
    
    
    def delete_spare_part(self,sparepart:spareParts):
        sparepart.delete(synchronize_session=False)
        self.db.commit()
            
    def get_spare_part_id(self, spare_part_id: UUID):
        spare_part=self.db.query(spareParts).filter(spareParts.spare_parts_id==spare_part_id)
        if not spare_part.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی لوازم یدکی با این شناسه موجود نیست")
        return spare_part  
    
    def update_spare_part_id(self, spare_part_id: UUID,data:json):
        
        self.db.query(spareParts).filter(spareParts.spare_parts_id==spare_part_id).update(data,synchronize_session=False)
        self.db.commit()

    