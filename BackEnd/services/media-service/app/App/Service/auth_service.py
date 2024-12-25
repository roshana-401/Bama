from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import requests

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://iam_service:80/TokenVerify")


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
    