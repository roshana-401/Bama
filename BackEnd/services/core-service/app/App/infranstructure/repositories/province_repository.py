
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.schemas.province_schema import (
    province_list
)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.city_and_province import province

class ProvinceRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db
        
    def create_province(self,provincee:province):
        self.get_province_name(provincee.province_name)
        self.db.add(provincee)
        self.db.commit()
        self.db.refresh(provincee)
        return provincee
    
    
    def delete_province(self,provincee:province):
        provincee.delete(synchronize_session=False)
        self.db.commit()
    
    def update_province(self,province_id:UUID,NewDetail:str):
        
        updated_province=self.get_province_id(province_id=province_id)
        self.get_province_name(NewDetail)
        updated_province.update({"province_name":NewDetail},synchronize_session=False)
        self.db.commit()
        return updated_province.first()

    def get_province_id(self, province_id: UUID):
        provincee=self.db.query(province).filter(province.province_id==province_id)
        if not provincee.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این شناسه موجود نیست")
        return provincee
        

    def get_province_name(self,name):
        province_name=self.db.query(province).filter(province.province_name==name)
        if province_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این نام موجود است")
        
        
    def get_all_province(self):
        provinces = self.db.query(province).all()
        return [province_list.from_orm(province) for province in provinces]
    
    def get_province_name_by_id(self,province_id:UUID):
        province_name=self.db.query(province).filter(province.province_id==province_id)
        if not province_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این شناسه موجود نیست")
        return province_name.first()
    
    def get_province_id_by_name(self,name):
        province_name=self.db.query(province).filter(province.province_name==name)
        if not province_name.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این نام موجود نیست")
        return province_name.first()