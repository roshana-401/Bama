from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.city_service import CityService
from uuid import UUID
from App.domain.schemas.city_schema import (
    Add_city,
    massage_city,
    massage,
    update_city,
    city_list,
    get_province_id,
    city_id,
    get_name
)

router=APIRouter(
    tags=["City"],
    prefix='/admin/city'
)




@router.post("/Add",response_model=massage_city,status_code=status.HTTP_201_CREATED)

async def AddCity(cityy:Add_city,
                        cityService:Annotated[CityService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")

    return await cityService.Add_city(cityy)


@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)

async def DeleteCity(city_id:str,
                        cityService:Annotated[CityService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    try:
        city_id=UUID(city_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    
    
    return await cityService.delete_city(city_id=city_id)


@router.post("/update",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdateCity(cityy:update_city,
                        cityService:Annotated[CityService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    
    
    return await cityService.update_city(city_id=cityy.city_id,newDetail=cityy.city_name)


@router.post("/getCityId",response_model=city_id,status_code=status.HTTP_200_OK)

async def getCityId(cityy:get_name,cityService:Annotated[CityService, Depends()]):
    
    return await cityService.get_city_id(city_name=cityy.city_name)



@router.post("/getAllProvinceCity",response_model=List[city_list],status_code=status.HTTP_200_OK)

async def getAllCity(province:get_province_id,cityService:Annotated[CityService, Depends()]):
    
    return await cityService.get_all_city(province_id=province.province_id)
