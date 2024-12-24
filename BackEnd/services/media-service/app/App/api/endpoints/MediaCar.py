from fastapi import status,Depends,APIRouter,UploadFile,HTTPException,File,Form
from typing import List,Annotated
from uuid import UUID
from App.Service.auth_service import getUser
from fastapi.responses import StreamingResponse
from App.domain.schemas.Media_schema import (
    MediaResponse
)
from App.domain.schemas.car_schema import (
    GetPictureCar
)
from App.Service.media_service import MediaServiceCar
import json

router=APIRouter(
    tags=["CarMedia"],
    prefix='/Media/Car'
)

# @router.get("/GetPicture",status_code=status.HTTP_200_OK)

# async def GetPictureCars(
#     # car:GetPictureCar,
#     informationUser: Annotated[json, Depends(getUser)],
# ):
#     print(informationUser["date_update_Profile"])
    
ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]    

@router.post(
    "/UploadMediaCar", response_model=MediaResponse, status_code=status.HTTP_201_CREATED
)
async def upload_media(
    file: Annotated[UploadFile, File()],
    car_sell_id:Annotated[UUID, Form()],
    media_service: Annotated[MediaServiceCar, Depends()],
    informationUser: Annotated[json, Depends(getUser)],
):
    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فقط فایل‌های تصویری با پسوند .jpegو .png و .webp مجاز هستند"
        )

    print("okoko")
    return await media_service.create_media_car(file, informationUser["user_id"],car_sell_id=str(car_sell_id))

    #request to cor to this user is owner this posts or not
    
        
@router.get("/GetMediaCar",response_class=StreamingResponse,status_code=status.HTTP_200_OK)

async def registerUser(mongo_id:GetPictureCar,
                       media_service: Annotated[MediaServiceCar, Depends()],
                       informationUser: Annotated[json, Depends(getUser)],):
    media, file = await media_service.get_madia_car(
        mongo_id=mongo_id.mongo_id, user_id=informationUser["user_id"]
    )
    return StreamingResponse(
        content=file(),
        media_type=media.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media.filename}"
        },
    )






# @router.post("/AddPicture",response_model=RegisterStepTwo,status_code=status.HTTP_200_OK)

# async def registerUser(user:VerifyOTPSchema,RegisterService:Annotated[RegisterService,Depends()]):
#     return await RegisterService.verify_user(user)


# @router.delete("/DeletePicture",response_model=RegisterStepThree,status_code=status.HTTP_201_CREATED)

# async def registerUser(user:UserRegister,RegisterService:Annotated[RegisterService,Depends()]):
#     return await RegisterService.create_user(user)
        


