
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import (get_db,get_db_user)
from fastapi import Depends,HTTPException,status
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.save_sell_car import (saveSellCar)
from sqlalchemy.dialects.postgresql import UUID

class SaveSellCarRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db

    def create_save_sell_car(self,save_sell_car:saveSellCar):
        self.db.add(save_sell_car)
        self.db.commit()
        self.db.refresh(save_sell_car)
        return save_sell_car
    
    
    def delete_save_sell_car(self,save_sell_car:saveSellCar):
        self.db.delete(save_sell_car)
        self.db.commit()
        
    def find_save_sell_car(self,save_sell_car:saveSellCar):
        print(save_sell_car.user_id)
        print(save_sell_car.sell_car_id)
        boolForExist = self.db.query(saveSellCar).filter(saveSellCar.user_id==save_sell_car.user_id,saveSellCar.sell_car_id==save_sell_car.sell_car_id)
        if boolForExist.first():
            return True
        else:
            return False
        
    def get_save_sell_car(self,save_sell_car:saveSellCar):
        boolForExist = self.db.query(saveSellCar).filter(saveSellCar.user_id==save_sell_car.user_id,saveSellCar.sell_car_id==save_sell_car.sell_car_id)
        if not boolForExist.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="این آگهی در لیست مورد علاقه ها وجود ندارد ")
        return boolForExist.first()
    
    def get_all_save_sell_car_by_ID(self,user_id:UUID):
        all_save_car = self.db.query(saveSellCar).filter(saveSellCar.user_id==user_id)

                                                                                                                    
        return all_save_car.all()
    
    