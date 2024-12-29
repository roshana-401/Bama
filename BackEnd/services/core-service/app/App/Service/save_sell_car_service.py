from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.models.save_sell_car import (saveSellCar)
from App.infranstructure.repositories.sell_car_repository import SellCarRepository
from App.infranstructure.repositories.user_repository import UserRepository
from App.infranstructure.repositories.save_sell_car_repository import SaveSellCarRepository
from App.Service.base_service import BaseService
from App.domain.schemas.save_sell_car_schema import (save_sell_car,massage,get_user_id,all_save_sell_car)

class SaveSellCarService(BaseService):
    def __init__(
        self,
        sell_car_repository: Annotated[SellCarRepository, Depends()],
        user_repository:Annotated[UserRepository,Depends()],
        save_sell_car_repository:Annotated[SaveSellCarRepository,Depends()],
        
    ) -> None:
        super().__init__()

        self.sell_car_repository = sell_car_repository
        self.user_repository=user_repository
        self.save_sell_car_repository=save_sell_car_repository
        
    async def existOrNot(self,save_sell_car:save_sell_car):
        self.user_repository.get_user_by_id(save_sell_car.user_id)
        self.sell_car_repository.get_sell_car_id(sell_car_id=save_sell_car.sell_car_id)
        
        save_sell=saveSellCar(
            user_id=save_sell_car.user_id,
            sell_car_id=save_sell_car.sell_car_id
        )
        
        if self.save_sell_car_repository.find_save_sell_car(save_sell):
            save=self.save_sell_car_repository.get_save_sell_car(save_sell)
            return await self.Delete_sell_car(save)
        else:
            return await self.Add_sell_car(save_sell)
        
    async def Add_sell_car(self,save_sell_car:saveSellCar):
        
        self.save_sell_car_repository.create_save_sell_car(save_sell_car)
        return massage(massage=" آگهی مورد نظر با موفقیت به مورد علاقه ها اضافه شد")

    async def Delete_sell_car(self,save_sell_car:saveSellCar):
        
        self.save_sell_car_repository.delete_save_sell_car(save_sell_car)
        return massage(massage=" آگهی مورد نظر با موفقیت از مورد علاقه ها حذف شد")
    
    async def get_all_save_sell_car(self,user_id:get_user_id):
        
        saves_car=self.save_sell_car_repository.get_all_save_sell_car_by_ID(user_id.user_id)
        
        return [all_save_sell_car(sell_car_id=save_car.sell_car_id) for save_car in saves_car]
        
