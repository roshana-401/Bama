from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.save_sell_spare_part_service import SaveSellSparePartService
from uuid import UUID
from App.Service.role_service import RoleService

from App.domain.schemas.save_sell_spare_part_schema import (
    massage,
    save_sell_spare_part,
    all_save_sell_spare_part,
    get_user_id,
    get_user_id_For_save
)
from App.domain.schemas.sell_spare_part import (
    sell_spare_part_form
)
router=APIRouter(
    tags=["SaveSellSparePart"],
    prefix='/SaveSellSparePart'
)




@router.post("/AddOrDelete",response_model=massage,status_code=status.HTTP_201_CREATED)

async def AddOrDeleteSaveSellCar(savesellsparePart:save_sell_spare_part,
                        saveSellSparePartService:Annotated[SaveSellSparePartService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)],
                       role:Annotated[RoleService, Depends()]):
    role_Admin=await role.get_role_admin()
    if savesellsparePart.user_id!=None and int(informationUser["role_id"])==int(role_Admin):
        return await saveSellSparePartService.existOrNot(save_sell_spare_part(sell_spare_part_id=savesellsparePart.sell_spare_part_id,user_id=savesellsparePart.user_id))
    
    else:
        return await saveSellSparePartService.existOrNot(save_sell_spare_part(sell_spare_part_id=savesellsparePart.sell_spare_part_id,user_id=informationUser["user_id"]))

@router.post("/getAllSellSparePart",response_model=List[sell_spare_part_form],status_code=status.HTTP_200_OK)
async def getSaveSellCarByID(user_id:get_user_id_For_save,
                        saveSellSparePartService:Annotated[SaveSellSparePartService, Depends()],
                        informationUser: Annotated[dict, Depends(getUser)],
                        role:Annotated[RoleService, Depends()]):
    role_Admin=await role.get_role_admin()
    if user_id.user_id!=None and int(informationUser["role_id"])==int(role_Admin):
        return await saveSellSparePartService.get_all_save_sell_spare_part(user_id=user_id.user_id)
    
    else:
        return await saveSellSparePartService.get_all_save_sell_spare_part(user_id=informationUser["user_id"])

