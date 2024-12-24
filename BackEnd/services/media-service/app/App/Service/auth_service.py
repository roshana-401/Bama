from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import json
import subprocess

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://iam.localhost/TokenVerify")


async def getUser(
    token: Annotated[str, Depends(oauth2_scheme)],
    ):
    print("mkmkmk")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="شما احراز هویت نیستید")
    else:
       curl_command = [
        "curl", "-v", 
        "http://iam.localhost/TokenVerify",
        "-H", f"Authorization: Bearer {token}",
        "-H", "User-Agent: Mozilla/5.0",  
        "-H", "Accept: application/json", 
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)        
        try:
            response = json.loads(result.stdout)
            if 'detail' in response:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="شما احراز هویت نیستید"
                )
            return response
        
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Response is not valid JSON."
            )
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Request failed using curl."
        )