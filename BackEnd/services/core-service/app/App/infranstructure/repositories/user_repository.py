
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import (get_db_user)
from fastapi import Depends,HTTPException,status
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.user import users

class UserRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db_user)]):
        self.db=db
        
    def get_user_by_id(self,user_id:UUID):
        user=self.db.query(users).filter(users.user_id==user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="  چنین کاربری وجود ندارد")
        return user.first()
        
        
        
    # def create_sell_car(self,sell_car:SellCar):
    #     self.db.add(sell_car)
    #     self.db.commit()
    #     self.db.refresh(sell_car)
    #     return sell_car
    
    
    # def delete_sell_car(self,sell_car:SellCar):
    #     sell_car.delete(synchronize_session=False)
    #     self.db.commit()
    
    # def update_sell_car_descrip(self,sell_car_id:UUID,NewDetail:update_description):
        
    #     updated_sell_car=self.get_sell_car_id(sell_car_id=sell_car_id)
    #     updated_sell_car.update({"description":NewDetail.description},synchronize_session=False)
    #     self.db.commit()
    #     return updated_sell_car.first()
    
    # def update_sell_car_phone_number(self,user_id:UUID,NewDetail:update_phone_number):
        
    #     updated_sell_car=self.get_sell_car_id(sell_car_id=sell_car_id)
    #     updated_sell_car.update({"description":NewDetail.description},synchronize_session=False)
    #     self.db.commit()
    #     return updated_sell_car.first()

    # def get_sell_car_id(self, sell_car_id: UUID):
    #     sell_car=self.db.query(SellCar).filter(SellCar.sell_car_id==sell_car_id)
    #     if not sell_car.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی ماشین با این شناسه موجود نیست")
    #     return sell_car
        

    # def get_province_name(self,name):
    #     province_name=self.db.query(province).filter(province.province_name==name)
    #     if province_name.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این نام موجود است")
        
        
    # def get_all_sell_car(self):
    #     provinces = self.db.query(province).all()
    #     return [province_list.from_orm(province) for province in provinces]
    
    # def get_province_name_by_id(self,province_id:UUID):
    #     province_name=self.db.query(province).filter(province.province_id==province_id)
    #     if not province_name.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این شناسه موجود نیست")
    #     return province_name.first()
    
    # def get_province_id_by_name(self,name):
    #     province_name=self.db.query(province).filter(province.province_name==name)
    #     if not province_name.first():
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" استان با این نام موجود نیست")
    #     return province_name.first()