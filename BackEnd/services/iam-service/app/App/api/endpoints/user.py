from fastapi import status,Depends,APIRouter,HTTPException
from typing import Annotated,List
from App.Service.auth_service.auth_service import AuthService
from App.Service.user_service import UserService
from App.Service.update_information_service import UpdateService
from App.Service.user_service import UserService

from uuid import UUID
from App.Service.role_service import RoleService
from App.Service.token_service import verify_token
from App.domain.models.user import users

from App.domain.schemas.user_schema import (
    user_list,
    massage,
    GetPhoneNumber,
    UserUpdatePhoneNumber,
    VerifyOTPSchema,
    updatePassword
)

router=APIRouter(
    tags=["User"],
    prefix='/user'
)




@router.get("/getAllUser",response_model=List[user_list],status_code=status.HTTP_200_OK)

async def getAllUSer(userService:Annotated[UserService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)],
                       role:Annotated[RoleService, Depends()]):
    
    if user_current.role_id!=await role.get_role_admin():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="کاربر اجازه دسترسی ندارد")

    return await userService.get_all_user()



@router.delete("/delete",response_model=massage,status_code=status.HTTP_200_OK)

async def DeleteUser(user_id:str,
                        userService:Annotated[UserService, Depends()],
                        user_current:Annotated[users,Depends(verify_token)],
                       role:Annotated[RoleService, Depends()]):
    
    if user_current.role_id!=await role.get_role_admin():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="کاربر اجازه دسترسی ندارد")
    try:
        user_id=UUID(user_id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="فرمت اشتباه است")
    
    
    return await userService.delete_user(user_id=user_id)



@router.post("/updatePhoneNumberStepOne",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdatePhoneStepOne(info:GetPhoneNumber,
                        updateService:Annotated[UpdateService, Depends()],
                        userService:Annotated[UserService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)]):
    
    user=await userService.get_user(user_current.user_id)
    if info.phone_number!=user.phone_number:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="شماره تلفن غیر مجاز")        
    
    return await updateService.UpdatePhoneNumberStepOne(info)


@router.post("/updatePhoneNumberStepTwo",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdatePhoneStepTwo(info:UserUpdatePhoneNumber,
                        updateService:Annotated[UpdateService, Depends()],
                        userService:Annotated[UserService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)]):
    
    user=await userService.get_user(user_current.user_id)
    if info.pass_phone_number!=user.phone_number:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="شماره تلفن غیر مجاز")        
    
    return await updateService.UpdatePhoneNumberStepTwo(info)


@router.post("/updatePhoneNumberStepThree",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdatePhoneStepThree(info:VerifyOTPSchema,
                        updateService:Annotated[UpdateService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)]):
        
    return await updateService.UpdatePhoneNumberStepThree(info,user_current.user_id)


@router.post("/resendOTPForUpdateStepTwo",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdatePhoneStepThree(info:GetPhoneNumber,
                        updateService:Annotated[UpdateService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)]):
    
    if user_current.phone_number!=info.phone_number:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="کاربر اجازه دسترسی ندارد")    
    return await updateService.resend_otp_update_phone_number_step_two(info)

@router.post("/resendOTPForUpdateStepThree",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdatePhoneStepThree(info:GetPhoneNumber,
                        updateService:Annotated[UpdateService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)]):
       
    return await updateService.resend_otp_update_phone_number_step_three(info,user_current.user_id)

@router.post("/updatePassword",response_model=massage,status_code=status.HTTP_200_OK)

async def UpdatePhoneStepThree(info:updatePassword,
                        updateService:Annotated[UpdateService, Depends()],
                       user_current:Annotated[users,Depends(verify_token)]):
       
    return await updateService.update_password(info,user_current.user_id)