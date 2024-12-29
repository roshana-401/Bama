from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.sell_spare_part_service import SellSparePartService
from uuid import UUID
from App.Service.role_service import RoleService

from App.domain.schemas.sell_spare_part import (
    massage,
    massage_sell_spare_part,
    Add_sell_spare_part_form,
    Add_sell_spare_part,
    get_sell_spare_part_id,
    sell_spare_part_form,
    filter_data_sell_spare_part,
    updata_sell_spare_part
)

router=APIRouter(
    tags=["SellSparePart"],
    prefix='/SellSparePart'
)




@router.post("/Add",response_model=massage_sell_spare_part,status_code=status.HTTP_201_CREATED)

async def AddSellSparePart(sell_spare_part_form:Add_sell_spare_part_form,
                        sellsparepartService:Annotated[SellSparePartService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):

    return await sellsparepartService.Add_sell_spare_part(Add_sell_spare_part(spare_part_name=sell_spare_part_form.spare_part_name,
                                                          model_id=sell_spare_part_form.model_id,
                                                          price=sell_spare_part_form.price,
                                                          Operation=sell_spare_part_form.Operation,
                                                          description=sell_spare_part_form.description,
                                                          city_id=sell_spare_part_form.city_id,
                                                          user_id=informationUser["user_id"]))

@router.post("/getSellSparePartById",response_model=sell_spare_part_form,status_code=status.HTTP_200_OK)
async def getSellSparePartById(sell_spare_part_id:get_sell_spare_part_id,
                        sellsparepartService:Annotated[SellSparePartService, Depends()]):
    return await sellsparepartService.get_sell_spare_part_id(sell_spare_part_id=sell_spare_part_id.sell_spare_part_id)


@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)
async def deleteSellSparePart(sell_spare_part_id:str,
                        sellsparepartService:Annotated[SellSparePartService, Depends()],
                        informationUser: Annotated[dict, Depends(getUser)],
                        role:Annotated[RoleService, Depends()]):
    try:
        sell_spare_part_id=UUID(sell_spare_part_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    
    role_Admin=await role.get_role_admin()
    user_id=UUID(informationUser["user_id"])
    return await sellsparepartService.delete_sell_spare_part_id(sell_spare_part_id=sell_spare_part_id,role_id=informationUser["role_id"],user_id=user_id,role_Admin=role_Admin)

@router.post("/getByFilter",response_model=List[sell_spare_part_form],status_code=status.HTTP_200_OK)
async def getFilterSellSparePart(sell_spare_part_filter_data:filter_data_sell_spare_part,
                        sellsparepartService:Annotated[SellSparePartService, Depends()],):
    
    return await sellsparepartService.get_sell_spare_part_with_filter(sell_spare_part_filter_data)

@router.post("/getSellSparePartId",status_code=status.HTTP_200_OK)
async def getSellCarId(sell_spare_part_id:get_sell_spare_part_id,
                        sellsparepartService:Annotated[SellSparePartService, Depends()],):
    
    return await sellsparepartService.get_sell_spare_part_id_for_check(sell_spare_part_id=sell_spare_part_id.sell_spare_part_id)

@router.post("/update",response_model=massage,status_code=status.HTTP_200_OK)
async def updateSellSparePart(sell_spare_part_update:updata_sell_spare_part,
                        sellsparepartService:Annotated[SellSparePartService, Depends()],
                        informationUser: Annotated[dict, Depends(getUser)],
                        role:Annotated[RoleService, Depends()]):
    
    role_Admin=await role.get_role_admin()
    user_id=UUID(informationUser["user_id"])
    return await sellsparepartService.update_sell_spare_part_id(newDetail=sell_spare_part_update,sell_spare_part_id=sell_spare_part_update.sell_spare_part_id,role_id=informationUser["role_id"],user_id=user_id,role_Admin=role_Admin)

