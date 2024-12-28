from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.sell_car_service import SellCarService
from uuid import UUID
from App.Service.role_service import RoleService

from App.domain.schemas.sell_car_schema import (
    massage,
    massage_sell_car,
    Add_sell_car_form,
    Add_sell_car,
    get_sell_car_id,
    sell_car_form,
    filter_data_sell_car,
    updata_sell_car
)

router=APIRouter(
    tags=["SellCar"],
    prefix='/SellCar'
)




@router.post("/Add",response_model=massage_sell_car,status_code=status.HTTP_201_CREATED)

async def AddSellCar(sell_car_form:Add_sell_car_form,
                        sellcarService:Annotated[SellCarService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):

    return await sellcarService.Add_sell_car(Add_sell_car(car_name=sell_car_form.car_name,
                                                          model_id=sell_car_form.model_id,
                                                          price=sell_car_form.price,
                                                          color=sell_car_form.color,
                                                          gearbox=sell_car_form.gearbox,
                                                          KM=sell_car_form.KM,
                                                          Operation=sell_car_form.Operation,
                                                          year=sell_car_form.year,
                                                          description=sell_car_form.description,
                                                          city_id=sell_car_form.city_id,
                                                          user_id=informationUser["user_id"]))

@router.post("/getSellCarById",response_model=sell_car_form,status_code=status.HTTP_200_OK)
async def getSellCarByID(sell_car_id:get_sell_car_id,
                        sellcarService:Annotated[SellCarService, Depends()]):
    return await sellcarService.get_sell_car_id(sell_car_id=sell_car_id.sell_car_id)


@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)
async def deleteSellCar(sell_car_id:str,
                        sellcarService:Annotated[SellCarService, Depends()],
                        informationUser: Annotated[dict, Depends(getUser)],
                        role:Annotated[RoleService, Depends()]):
    try:
        sell_car_id=UUID(sell_car_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    role_Admin=await role.get_role_admin()
    user_id=UUID(informationUser["user_id"])
    return await sellcarService.delete_sell_car_id(sell_car_id=sell_car_id,role_id=informationUser["role_id"],user_id=user_id,role_Admin=role_Admin)

@router.post("/getByFilter",response_model=List[sell_car_form],status_code=status.HTTP_200_OK)
async def deleteSellCar(sell_car_filter_data:filter_data_sell_car,
                        sellcarService:Annotated[SellCarService, Depends()],):
    
    return await sellcarService.get_sell_car_with_filter(sell_car_filter_data)
    

@router.post("/update",response_model=massage,status_code=status.HTTP_200_OK)
async def deleteSellCar(sell_car_update:updata_sell_car,
                        sellcarService:Annotated[SellCarService, Depends()],
                        informationUser: Annotated[dict, Depends(getUser)],
                        role:Annotated[RoleService, Depends()]):
    
    role_Admin=await role.get_role_admin()
    user_id=UUID(informationUser["user_id"])
    return await sellcarService.update_sell_car_id(newDetail=sell_car_update,sell_car_id=sell_car_update.sell_car_id,role_id=informationUser["role_id"],user_id=user_id,role_Admin=role_Admin)

