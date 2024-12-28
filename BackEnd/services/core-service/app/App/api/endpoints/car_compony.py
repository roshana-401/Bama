from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import getUser
from App.Service.car_compony_service import CarComponyService
from uuid import UUID
from App.domain.schemas.car_compony_schema import (
    Add_car_compony,
    massage_car_compony,
    massage,
    update_car_compony,
    car_compony_list,
    compony_car_id,
    get_name
)

router=APIRouter(
    tags=["Car Compony"],
    prefix='/admin/carCompony'
)




@router.post("/Add",response_model=massage_car_compony,status_code=status.HTTP_201_CREATED)

async def AddCarCompony(car:Add_car_compony,
                        carComponyService:Annotated[CarComponyService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")

    return await carComponyService.Add_car_compony(car)

@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)

async def DeleteCarCompony(car_compony_id:str,
                        carComponyService:Annotated[CarComponyService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    try:
        car=UUID(car_compony_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    
    
    return await carComponyService.delete_car_compony(car)

@router.post("/update",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdateCarCompony(car_compony:update_car_compony,
                        carComponyService:Annotated[CarComponyService, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if informationUser["role_id"]!=1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="کاربر اجازه دسترسی ندارد")
    
    
    return await carComponyService.update_car_compony(car_compony.car_compony_id,car_compony.car_compony_name)

@router.get("/getAll",response_model=List[car_compony_list],status_code=status.HTTP_200_OK)

async def getAllCarCompony(carComponyService:Annotated[CarComponyService, Depends()]):
    
    return await carComponyService.get_all_car_compony()

@router.post("/getCarComponyId",response_model=compony_car_id,status_code=status.HTTP_200_OK)

async def getModelCarId(car_compony:get_name,carComponyService:Annotated[CarComponyService, Depends()]):
    
    return await carComponyService.get_car_compony_id(car_compony.car_compony_name)


