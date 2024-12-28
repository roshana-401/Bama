from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.province_service import ProvinceService
from uuid import UUID
from App.Service.role_service import RoleService

from App.domain.schemas.province_schema import (
    Add_province,
    massage_province,
    massage,
    update_province,
    province_list,
    province_id,
    get_name
)

router=APIRouter(
    tags=["Province"],
    prefix='/admin/province'
)




@router.post("/Add",response_model=massage_province,status_code=status.HTTP_201_CREATED)

async def AddProvince(province:Add_province,
                        provinceService:Annotated[ProvinceService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)],
                       role:Annotated[RoleService, Depends()]):
    
    if informationUser["role_id"]!=await role.get_role_admin():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")

    return await provinceService.Add_province(province)



@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)

async def DeleteProvince(province_id:str,
                        provinceService:Annotated[ProvinceService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)],
                       role:Annotated[RoleService, Depends()]):
    if informationUser["role_id"]!=await role.get_role_admin():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    try:
        province_id=UUID(province_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    
    
    return await provinceService.delete_province(province_id)



@router.post("/update",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdateProvice(province:update_province,
                        provinceService:Annotated[ProvinceService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)],
                       role:Annotated[RoleService, Depends()]):
    if informationUser["role_id"]!=await role.get_role_admin():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    
    
    return await provinceService.update_province(province_id=province.province_id,newDetail=province.province_name)



@router.get("/getAll",response_model=List[province_list],status_code=status.HTTP_200_OK)

async def getAllProvince(provinceService:Annotated[ProvinceService, Depends()]):
    
    return await provinceService.get_all_province()



@router.post("/getProvinceId",response_model=get_name,status_code=status.HTTP_200_OK)

async def getProvinceId(province:province_id,provinceService:Annotated[ProvinceService, Depends()]):
    
    return await provinceService.get_province_id(province.province_id)


