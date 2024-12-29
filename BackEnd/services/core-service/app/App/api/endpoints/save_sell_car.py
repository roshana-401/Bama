from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.save_sell_car_service import SaveSellCarService
from uuid import UUID
from App.Service.role_service import RoleService

from App.domain.schemas.save_sell_car_schema import (
    massage,
    save_sell_car,
    all_save_sell_car,
    get_user_id
)

router=APIRouter(
    tags=["SaveSellCar"],
    prefix='/SaveSellCar'
)




@router.post("/AddOrDelete",response_model=massage,status_code=status.HTTP_201_CREATED)

async def AddOrDeleteSaveSellCar(savesellcar:save_sell_car,
                        saveSellCarService:Annotated[SaveSellCarService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)],
                       role:Annotated[RoleService, Depends()]):
    role_Admin=await role.get_role_admin()
    if savesellcar.user_id!=None and int(informationUser["role_id"])==int(role_Admin):
        return await saveSellCarService.existOrNot(save_sell_car(sell_car_id=savesellcar.sell_car_id,user_id=savesellcar.user_id))
    
    else:
        return await saveSellCarService.existOrNot(save_sell_car(sell_car_id=savesellcar.sell_car_id,user_id=informationUser["user_id"]))

@router.post("/getAllSellCarById",response_model=List[all_save_sell_car],status_code=status.HTTP_200_OK)
async def getSaveSellCarByID(user_id:get_user_id,
                        saveSellCarService:Annotated[SaveSellCarService, Depends()],
                        informationUser: Annotated[dict, Depends(getUser)],
                        role:Annotated[RoleService, Depends()]):
    role_Admin=await role.get_role_admin()

    if informationUser["role_id"]!=role_Admin and user_id.user_id!=UUID(informationUser["user_id"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")        
    return await saveSellCarService.get_all_save_sell_car(user_id=user_id)

