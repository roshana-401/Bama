from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import requests
from uuid import UUID
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://iam_service:80/user/Login")


async def getUser(
    token: Annotated[str, Depends(oauth2_scheme)],
    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="شما احراز هویت نیستید")
    else:
        header={
            "Authorization": f"Bearer {token}",
        }
        response=requests.get("http://iam_service:80/TokenVerify",headers=header)
        
        if response.status_code==401:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="شما اهراز هویت نیستید ",
                                            headers={"WWW-Authenticate":"Bearer"})
        return response.json()
    
async def getinfoSellCar(sell_car_id:str):
    
        response=requests.post("http://core_service:80/SellCar/getSellCarId",json={"sell_car_id":str(sell_car_id)})
        
        if response.status_code==400:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی ماشین با این شناسه موجود نیست")
        
        return response.json()
    
async def getinfoSellSparePart(sell_spare_part_id:str):
    
        response=requests.post("http://core_service:80/SellSparePart/getSellSparePartId",json={"sell_spare_part_id":str(sell_spare_part_id)})
        
        if response.status_code==400:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" آگهی لوازم یدکی با این شناسه موجود نیست")
        
        return response.json()
    