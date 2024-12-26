from fastapi import status,Depends,APIRouter,UploadFile,HTTPException,File,Form
from typing import List,Annotated
from uuid import UUID
from App.Service.auth_service import getUser
from fastapi.responses import StreamingResponse
from bson import ObjectId
from App.domain.schemas.spare_part_schema import (
    GetPictureSpare,
    massageSparePart,
    deletePictureSpare,
    GetAllMedia
)
from App.domain.schemas.Media_schema import (
    MediaResponse
)
from App.Service.media_service import MediaServiceSpareParts

router=APIRouter(
    tags=["SparePartsMedia"],
    prefix='/Media/SpareParts'
)


ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg","image/jpg", "image/png", "image/webp"]    
# MAX_FILE_SIZE = 5 * 1024 * 1024 
MAX_FILE_SIZE = 1 * 1024 * 1024 

@router.post(
    "/UploadMediaSparePart", response_model=MediaResponse, status_code=status.HTTP_201_CREATED
)
async def upload_media(
    file: Annotated[UploadFile, File()],
    spare_part_sell_id:Annotated[UUID, Form()],
    media_service: Annotated[MediaServiceSpareParts, Depends()],
    informationUser: Annotated[dict, Depends(getUser)],
):
    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="فقط فایل‌های تصویری با پسوند .jpegو jpg و.png و .webp مجاز هستند"
        )

    file_size = len(await file.read())
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"است MBحجم فایل بیشتر از حد مجاز است. حداکثر حجم مجاز 5",
        )
        
    return await media_service.create_media_sparePart(file, informationUser["user_id"],sell_spareparts_id=str(spare_part_sell_id))

    #request to cor to this user is owner this posts or not
    
    
@router.post("/GetMediaSparePart",response_class=StreamingResponse,status_code=status.HTTP_200_OK)

async def GetMedia(mongo_id:GetPictureSpare,
                       media_service: Annotated[MediaServiceSpareParts, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)],):
    media, file = await media_service.get_madia_sparePart(
        mongo_id=mongo_id.mongo_id, user_id=informationUser["user_id"]
    )
    return StreamingResponse(
        content=file(),
        media_type=media.content_type,
        headers={
            "Content-Disposition": f"attachment; filename={media.filename}"
        },
    )    

@router.delete("/DeleteMediaSparePart",response_model=massageSparePart,status_code=status.HTTP_200_OK)

async def DeleteMedia(mongo_id:str,
                       media_service: Annotated[MediaServiceSpareParts, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    if not ObjectId.is_valid(mongo_id):
            raise HTTPException(status_code=400, detail="فرمت اشتباه است")
        
    massage=await media_service.delete_madia_sparePart(mongo_id=ObjectId(mongo_id),user_id=informationUser["user_id"])
    
    return massageSparePart(massage=massage["massage"])  


@router.post("/GetAllMediaIdSpareParts",status_code=status.HTTP_200_OK)

async def GetAllMediaId(sparepart:GetAllMedia,
                       media_service: Annotated[MediaServiceSpareParts, Depends()],
                       informationUser: Annotated[dict, Depends(getUser)]):
    return await media_service.get_all_madia_spareParts(
        sell_spareparts_id=str(sparepart.sell_spareparts_id),user_id=informationUser["user_id"]
    )
        


