from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.domain.models.city_and_province import province
from App.infranstructure.repositories.province_repository import ProvinceRepository
from App.Service.base_service import BaseService
from App.domain.schemas.province_schema import (Add_province,massage_province,massage,get_province_id)
from uuid import UUID

class ProvinceService(BaseService):
    def __init__(
        self,
        province_repository: Annotated[ProvinceRepository, Depends()],
    ) -> None:
        super().__init__()

        self.province_repository = province_repository
        
    async def Add_province(self,provincee:Add_province):
        provincce=province(
            province_name=provincee.province_name
        )
        province_save=self.province_repository.create_province(provincce)
        return massage_province(massage=" استان مورد نظر با موفقیت اضافه شد",province_id=province_save.province_id)

    async def delete_province(self,province_id:UUID):
        provincee= self.province_repository.get_province_id(province_id)
        self.province_repository.delete_province(provincee)
        return massage(massage="استان مورد نظر با موفقیت حذف شد")
    
    async def update_province(self,province_id:UUID,newDetail:str):
        self.province_repository.update_province(province_id=province_id,NewDetail=newDetail)
        return massage(massage=" استان مورد نظر با موفقیت بروز شد")
    
    async def get_all_province(self):
        provinces=self.province_repository.get_all_province()
        return provinces
    
    async def get_province_id(self,province_name:str):
        province=self.province_repository.get_province_id_by_name(province_name)
        return get_province_id(province_id=province.province_id)