from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.model_car_service import ModelCarService
from uuid import UUID
from App.domain.schemas.model_car_schema import (
    Add_model_car,
    massage_model_car,
    massage,
    update_model_car,
    model_car_list,
    get_car_compony_id,
    model_car_id,
    get_name
)

router=APIRouter(
    tags=["Model Car"],
    prefix='/admin/modelCar'
)




@router.post("/Add",response_model=massage_model_car,status_code=status.HTTP_201_CREATED)

async def AddModelCar(model_car:Add_model_car,
                        modelCarService:Annotated[ModelCarService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")

    return await modelCarService.Add_model_car(model_car)

@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)

async def DeleteModelCar(model_car_id:str,
                        modelCarService:Annotated[ModelCarService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    try:
        model_car_id=UUID(model_car_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    
    
    return await modelCarService.delete_model_car(model_car_id)


@router.post("/update",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdateModelCar(model_car:update_model_car,
                        modelCarService:Annotated[ModelCarService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    
    
    return await modelCarService.update_model_car(model_car.model_id,model_car.model_car_name)


@router.post("/getCarModelId",response_model=model_car_id,status_code=status.HTTP_200_OK)

async def getModelCarId(model_car:get_name,modelCarService:Annotated[ModelCarService, Depends()]):
    
    return await modelCarService.get_model_car_id(car_model_name=model_car.model_car_name)



@router.post("/getAllCarComponyModel",response_model=List[model_car_list],status_code=status.HTTP_200_OK)

async def getAllModelCar(car_compony:get_car_compony_id,modelCarService:Annotated[ModelCarService, Depends()]):
    
    return await modelCarService.get_all_model_compony(car_compony_id=car_compony.car_compony_id)
