from fastapi import status,Depends,APIRouter
from App.domain.models.user import users
from App.core.config import setting
from App.Service.token_service import verify_token
from App.domain.schemas.user_schema import (
    UserSchema,
    
)

router=APIRouter(
    tags=["Token"],
)

@router.get("/TokenVerify",response_model=UserSchema,status_code=status.HTTP_200_OK)

async def Me(user_current:users=Depends(verify_token)):
    print("dndjnjenj")
    return user_current
