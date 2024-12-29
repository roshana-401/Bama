
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import Integer,cast,case,or_
from App.core.db.database import (get_db,get_db_user)
from fastapi import Depends,HTTPException,status
from App.domain.schemas.sell_spare_part import (updata_sell_spare_part,update_phone_number,filter_data_sell_spare_part)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.sell_spare_part import (SellSpareParts,spareParts)
from App.domain.models.model_and_car_compony import (car_compony,model)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.city_and_province import (city)
from App.infranstructure.repositories.user_repository import UserRepository
from App.infranstructure.repositories.spare_part_repository import SparePartRepository
from datetime import datetime
from sqlalchemy.orm import joinedload

class SellSparePartRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)],user_repository:Annotated[UserRepository,Depends()],
                 spare_part_repository:Annotated[SparePartRepository,Depends()]):
        self.db=db
        self.user_repository=user_repository
        self.spare_part_repository=spare_part_repository

    def create_sell_spare_part(self,sell_spare_part:SellSpareParts):
        self.db.add(sell_spare_part)
        self.db.commit()
        self.db.refresh(sell_spare_part)
        return sell_spare_part
    
    
    def delete_sell_spare_part(self,sell_spare_part:SellSpareParts):
        self.db.delete(sell_spare_part)
        self.db.commit()
    
    def update_sell_spare_part(self,updated_sell_spare_part:SellSpareParts,NewDetail:updata_sell_spare_part):
        
        
        if NewDetail.description!=None:
            updated_sell_spare_part.description = NewDetail.description  
            updated_sell_spare_part.date_update = datetime.utcnow()  
            self.db.commit()
        
        
        update_data = {}
    
        if NewDetail.spare_part_name is not None:
            update_data["spare_parts_name"] = NewDetail.spare_part_name
        if NewDetail.model_id is not None:
            update_data["model_id"] = NewDetail.model_id
        if NewDetail.price is not None:
            update_data["price"] = NewDetail.price
        if NewDetail.Operation is not None:
            update_data["Operation"] = NewDetail.Operation
        if NewDetail.city_id is not None:
            city = NewDetail.city_id
            updated_sell_spare_part.city_id=city
        
        if update_data: 
            updated_sell_spare_part.date_update=datetime.utcnow()
            
            self.spare_part_repository.update_spare_part_id(updated_sell_spare_part.spare_parts_id,data=update_data)
            self.db.commit()
        
        return updated_sell_spare_part
    
    def update_sell_spare_part_phone_number(self,user_id:UUID,NewDetail:update_phone_number):
        
        self.user_repository.get_user_by_id(user_id=user_id)
        self.db.query(SellSpareParts).filter(SellSpareParts.user_id==user_id).update({"phone_number":NewDetail.phone_number},synchronize_session=False)
        
        self.db.commit()


    def get_sell_spare_part_id(self, sell_spare_part_id: UUID):
        sell_spare_part = self.db.query(SellSpareParts).options(joinedload(SellSpareParts.spare_parts).joinedload(spareParts.model).joinedload(model.car_compony) ).options(joinedload(SellSpareParts.city).joinedload(city.province)).filter(SellSpareParts.sell_spare_parts_id == sell_spare_part_id)
        if not sell_spare_part.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی لوازم یدکی با این شناسه موجود نیست")
        return sell_spare_part.first()
        
        
    def get_sell_spare_part_id_and_check(self,sell_spare_part_id: UUID):
        sell_spare_part=self.db.query(SellSpareParts).filter(SellSpareParts.sell_spare_parts_id==sell_spare_part_id)
        if not sell_spare_part.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی ماشین با این شناسه موجود نیست")
        return sell_spare_part.first()
        
    def get_all_sell_spare_part(self,filter_data:filter_data_sell_spare_part):
        sells_spare_part = self.db.query(SellSpareParts).options(joinedload(SellSpareParts.spare_parts).joinedload(spareParts.model).joinedload(model.car_compony) ).options(joinedload(SellSpareParts.city).joinedload(city.province)).filter(
                                                                                                                                                                                                    
                                                                                                                                                                                                      case((filter_data.model_id is not None, SellSpareParts.spare_parts.has(spareParts.model_id==filter_data.model_id)),else_=True),
                                                                                                                                                                                                      case((filter_data.car_compony_id is not None, model.car_compony.has(model.car_compony_id==filter_data.car_compony_id)),else_=True),
                                                                                                                                                                                                      SellSpareParts.spare_parts.has(spareParts.spare_parts_name.contains(filter_data.spare_part_name)),
                                                                                                                                                                                                      SellSpareParts.spare_parts.has(cast(spareParts.price,Integer)>=filter_data.price_down),
                                                                                                                                                                                                        SellSpareParts.spare_parts.has(cast(spareParts.price,Integer)<=filter_data.price_top)
                                                                                                                                                                                                    )

                                                                                                                    
        return sells_spare_part.all()
    
    