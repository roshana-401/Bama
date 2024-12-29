from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.models.save_sell_spare_part import (saveSellSparePart)
from App.infranstructure.repositories.sell_spare_parts_repository import SellSparePartRepository
from App.infranstructure.repositories.user_repository import UserRepository
from App.infranstructure.repositories.save_sell_spare_part_repository import SaveSellSparePartRepository
from App.Service.base_service import BaseService
from App.domain.schemas.save_sell_spare_part_schema import (save_sell_spare_part,massage,get_user_id,all_save_sell_spare_part)

class SaveSellSparePartService(BaseService):
    def __init__(
        self,
        sell_spare_part_repository: Annotated[SellSparePartRepository, Depends()],
        user_repository:Annotated[UserRepository,Depends()],
        save_sell_spare_part_repository:Annotated[SaveSellSparePartRepository,Depends()],
        
    ) -> None:
        super().__init__()

        self.sell_spare_part_repository = sell_spare_part_repository
        self.user_repository=user_repository
        self.save_sell_spare_part_repository=save_sell_spare_part_repository
        
    async def existOrNot(self,save_sell_spare_part:save_sell_spare_part):
        self.user_repository.get_user_by_id(save_sell_spare_part.user_id)
        self.sell_spare_part_repository.get_sell_spare_part_id(sell_spare_part_id=save_sell_spare_part.sell_spare_part_id)
        
        save_sell=saveSellSparePart(
            user_id=save_sell_spare_part.user_id,
            sell_spare_parts_id=save_sell_spare_part.sell_spare_part_id
        )
        
        if self.save_sell_spare_part_repository.find_save_sell_spare_part(save_sell):
            save=self.save_sell_spare_part_repository.get_save_sell_spare_part(save_sell)
            return await self.Delete_sell_spare_part(save)
        else:
            return await self.Add_sell_spare_part(save_sell)
        
    async def Add_sell_spare_part(self,save_sell_spare_part:saveSellSparePart):
        
        self.save_sell_spare_part_repository.create_save_sell_spare_part(save_sell_spare_part)
        return massage(massage=" آگهی مورد نظر با موفقیت به مورد علاقه ها اضافه شد")

    async def Delete_sell_spare_part(self,save_sell_spare_part:saveSellSparePart):
        
        self.save_sell_spare_part_repository.delete_save_sell_spare_part(save_sell_spare_part)
        return massage(massage=" آگهی مورد نظر با موفقیت از مورد علاقه ها حذف شد")
    
    async def get_all_save_sell_spare_part(self,user_id:get_user_id):
        
        saves_sparepart=self.save_sell_spare_part_repository.get_all_save_sell_spare_part_by_ID(user_id.user_id)
        
        return [all_save_sell_spare_part(sell_spare_part_id=save_sparepart.sell_spare_parts_id) for save_sparepart in saves_sparepart]
        
