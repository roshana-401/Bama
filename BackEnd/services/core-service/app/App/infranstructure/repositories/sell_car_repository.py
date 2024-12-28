
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import Integer,cast,case,or_
from App.core.db.database import (get_db,get_db_user)
from fastapi import Depends,HTTPException,status
from App.domain.schemas.sell_car_schema import (updata_sell_car,update_phone_number,filter_data_sell_car)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.sell_car import (SellCar,car)
from App.domain.models.model_and_car_compony import (car_compony,model)
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.city_and_province import (city)
from App.infranstructure.repositories.user_repository import UserRepository
from App.infranstructure.repositories.city_repository import CityRepository
from App.infranstructure.repositories.model_car_repository import ModelCarRepository
from App.infranstructure.repositories.car_repository import CarRepository
from datetime import datetime
from sqlalchemy.orm import joinedload

class SellCarRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)],user_repository:Annotated[UserRepository,Depends()],
                 model_repository:Annotated[ModelCarRepository,Depends()],city_repository:Annotated[CityRepository,Depends()],
                 car_repository:Annotated[CarRepository,Depends()]):
        self.db=db
        self.user_repository=user_repository
        self.model_repository=model_repository
        self.city_repository=city_repository
        self.car_repository=car_repository

    def create_sell_car(self,sell_car:SellCar):
        self.db.add(sell_car)
        self.db.commit()
        self.db.refresh(sell_car)
        return sell_car
    
    
    def delete_sell_car(self,sell_car:SellCar):
        self.db.delete(sell_car)
        self.db.commit()
    
    def update_sell_car(self,updated_sell_car:SellCar,NewDetail:updata_sell_car):
        
        
        if NewDetail.description!=None:
            updated_sell_car.description = NewDetail.description  
            updated_sell_car.date_update = datetime.utcnow()  
            self.db.commit()
        
        
        update_data = {}
    
        if NewDetail.car_name is not None:
            update_data["car_name"] = NewDetail.car_name
        if NewDetail.model_id is not None:
            update_data["model_id"] = NewDetail.model_id
        if NewDetail.price is not None:
            update_data["price"] = NewDetail.price
        if NewDetail.color is not None:
            update_data["color"] = NewDetail.color
        if NewDetail.gearbox is not None:
            update_data["gearbox"] = NewDetail.gearbox
        if NewDetail.KM is not None:
            update_data["KM"] = NewDetail.KM
        if NewDetail.Operation is not None:
            update_data["Operation"] = NewDetail.Operation
        if NewDetail.year is not None:
            update_data["year"] = NewDetail.year
        if NewDetail.city_id is not None:
            city = NewDetail.city_id
            updated_sell_car.city_id=city
        
        if update_data: 
            updated_sell_car.date_update=datetime.utcnow()
            
            self.car_repository.update_car_id(updated_sell_car.car_id,data=update_data)
            self.db.commit()
        
        return updated_sell_car
    
    def update_sell_car_phone_number(self,user_id:UUID,NewDetail:update_phone_number):
        
        self.user_repository.get_user_by_id(user_id=user_id)
        self.db.query(SellCar).filter(SellCar.user_id==user_id).update({"phone_number":NewDetail.phone_number},synchronize_session=False)
        
        self.db.commit()


    def get_sell_car_id(self, sell_car_id: UUID):
        sell_car = self.db.query(SellCar).options(joinedload(SellCar.car).joinedload(car.model).joinedload(model.car_compony) ).options(joinedload(SellCar.city).joinedload(city.province)).filter(SellCar.sell_car_id == sell_car_id)
        if not sell_car.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی ماشین با این شناسه موجود نیست")
        return sell_car.first()
        
    def get_all_sell_car(self,filter_data:filter_data_sell_car):
        sells_car = self.db.query(SellCar).options(joinedload(SellCar.car).joinedload(car.model).joinedload(model.car_compony) ).options(joinedload(SellCar.city).joinedload(city.province)).filter(
                                                                                                                                                                                                    
                                                                                                                                                                                                      case((filter_data.model_id is not None, SellCar.car.has(car.model_id==filter_data.model_id)),else_=True),
                                                                                                                                                                                                      case((filter_data.car_compony_id is not None, model.car_compony.has(model.car_compony_id==filter_data.car_compony_id)),else_=True),
                                                                                                                                                                                                      case((filter_data.gearbox is not None, SellCar.car.has(car.gearbox==filter_data.gearbox)),else_=True),
                                                                                                                                                                                                      SellCar.car.has(car.car_name.contains(filter_data.car_name)),
                                                                                                                                                                                                      case((filter_data.year is not None, SellCar.car.has(cast(car.year,Integer)==filter_data.year)),else_=True),
                                                                                                                                                                                                      SellCar.car.has(cast(car.price,Integer)>=filter_data.price_down),
                                                                                                                                                                                                      SellCar.car.has(cast(car.KM,Integer)>=filter_data.KM_down),
                                                                                                                                                                                                        SellCar.car.has(cast(car.KM,Integer)<=filter_data.KM_top),
                                                                                                                                                                                                        SellCar.car.has(cast(car.price,Integer)<=filter_data.price_top)
                                                                                                                                                                                                    )

                                                                                                                    
        return sells_car.all()
    
    