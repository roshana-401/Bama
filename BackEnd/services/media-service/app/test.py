import pytest
import pytest_asyncio
from fastapi import status
from App.main import app
import httpx
import aiofiles


async def open_image_file(path: str):
    async with aiofiles.open(path, 'rb') as f:
        return await f.read()

async def get_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://iam_service:80/user/Login",
            data={"username": "09115728140", "password": "123456213"}
        )
        response_data = response.json()
        return response_data["Token"]
    
async def get_token2():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://iam_service:80/user/Login",
            data={"username": "09117865508", "password": "123456213"}
        )
        response_data = response.json()
        return response_data["Token"]
    

@pytest.mark.asyncio
async def test_get_Wrong_media_car():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media_service:80/Media/Car/GetMediaCar",
            json={"mongo_id": "676c1226f69bcb10c217432b"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    

@pytest.mark.asyncio
async def test_get_Wrong_media_spare_part():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media_service:80/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id": "676c2fe82a191a9c1f96a839"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_Wrong_user_media_car():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/GetMediaCar",
            json={"mongo_id":"67875b03477b9b430410eaa7"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_get_Wrong_user_media_spare():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id":"67875af0477b9b430410eaa2"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
@pytest.mark.asyncio
async def test_get_media_spare_and_car():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id":"67875d8942b1c754de55e727"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        response =await client.post(
            "http://media_service:80/Media/Car/GetMediaCar",
            json={"mongo_id":"67875c98ecb55c6f5c8f20d3"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        
@pytest.mark.asyncio
async def test_get_media_spare_and_car_admin():
    token=await get_token2()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id":"67875d8942b1c754de55e727"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        response =await client.post(
            "http://media_service:80/Media/Car/GetMediaCar",
            json={"mongo_id":"67875c98ecb55c6f5c8f20d3"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_upload_media_for_not_exist_spare_part():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media_service:80/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f660"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_upload_media_for_not_exist_car():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/UploadMediaCar",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"car_sell_id":"ee89f29d-c249-4f5f-aeb2-d579bd4821e0"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
@pytest.mark.asyncio
async def test_upload_no_access_media_spare_part():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media_service:80/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"658389b4-0ce3-485f-ba76-2aca7854e9be"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_upload_no_access_media_car():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/UploadMediaCar",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"car_sell_id":"b1bdd82e-2b7e-4915-8630-2c582c68d6ae"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.asyncio
async def test_upload_Wrong_media_size_spare_part():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media_service:80/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_upload_Wrong_media_size_car():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/UploadMediaCar",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"car_sell_id":"ee89f29d-c249-4f5f-aeb2-d579bd4821e2"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    

@pytest.mark.asyncio
async def test_upload_Wrong_media_format_spare_part():
    token=await get_token()
    file=await open_image_file("character.mp3")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media_service:80/Media/SpareParts/UploadMediaSparePart",
            files={"file":("character.mp3", file,"file/mp3")},  
            data={"spare_part_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_upload_Wrong_media_format_car():
    token=await get_token()
    file=await open_image_file("character.mp3")
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/UploadMediaCar",
            files={"file":("character.mp3", file,"file/mp3")},  
            data={"car_sell_id":"ee89f29d-c249-4f5f-aeb2-d579bd4821e2"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST    
        
    
@pytest.mark.asyncio
async def test_delete_Wrong_media():
    token=await get_token()    
    async with httpx.AsyncClient() as client:
        response =await client.delete(
            "http://media_service:80/Media/Car/DeleteMediaCar",
            params={"mongo_id":"676c1226f69bcb10c217432b"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response =await client.delete(
            "http://media_service:80/Media/SpareParts/DeleteMediaSparePart",
            params={"mongo_id":"676c2fe82a191a9c1f96a839"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_delete_Wrong_user_media():
    token=await get_token()    
    async with httpx.AsyncClient() as client:
        response =await client.delete(
            "http://media_service:80/Media/Car/DeleteMediaCar",
            params={"mongo_id":"6771a39e469881cf5b991065"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response =await client.delete(
            "http://media_service:80/Media/SpareParts/DeleteMediaSparePart",
            params={"mongo_id":"6771a35b469881cf5b991060"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
@pytest.mark.asyncio
async def test_upload_and_delete_media_car():
    token=await get_token()    
    file=await open_image_file("file.jpg")
    
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/UploadMediaCar",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"car_sell_id":"5f243695-7b64-426d-aeb2-12f7ac770bf8"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]

        response =await client.delete(
            "http://media_service:80/Media/Car/DeleteMediaCar",
            params={"mongo_id":result},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        
        
@pytest.mark.asyncio
async def test_upload_and_delete_media_car_admin():
    token=await get_token2()    
    file=await open_image_file("file.jpg")
    
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/UploadMediaCar",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"car_sell_id":"5f243695-7b64-426d-aeb2-12f7ac770bf8"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]

        response =await client.delete(
            "http://media_service:80/Media/Car/DeleteMediaCar",
            params={"mongo_id":result},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_upload_and_delete_media_spare_part():
    token=await get_token()    
    file=await open_image_file("file.jpg")
    
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"e130d4eb-8015-41dd-b68c-aa491033450f"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]
        
        response =await client.delete(
            "http://media_service:80/Media/SpareParts/DeleteMediaSparePart",
            params={"mongo_id":result},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        
@pytest.mark.asyncio
async def test_upload_and_delete_media_spare_part_admin():
    token=await get_token2()    
    file=await open_image_file("file.jpg")
    
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"e130d4eb-8015-41dd-b68c-aa491033450f"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]
        
        response =await client.delete(
            "http://media_service:80/Media/SpareParts/DeleteMediaSparePart",
            params={"mongo_id":result},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_all_Wrong_media():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        
        response =await client.post(
            "http://media_service:80/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"ee89f29d-c249-4f5f-aeb2-d579bd4821e2"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"5ebfbc92-5bfa-4074-9a17-62b4db51ad7a"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
@pytest.mark.asyncio
async def test_get_all_media_car_spare_part():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"b515da31-6581-4752-baa1-c51c2f8b4f60"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK

        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"2b5b062f-75fd-474f-972e-943d0ad7f2df"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        
@pytest.mark.asyncio
async def test_get_all_media_car_spare_part_admin():
    token=await get_token2()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"459590ad-086d-4659-830b-426ec3e410f6"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK

        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"c9979ad7-212c-4fbe-b2ce-c29dffa3dba4"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_all_media_car_spare_part_no_exist():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"48edf94e-312d-47d4-8a44-91df2b1f5690"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"38522a1e-99db-4bb0-9617-d0cd887300e0"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_get_all_media_car_spare_part_no_access():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media_service:80/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"c6e43e94-4108-4cd6-a6fb-2e917b2e7177"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response =await client.post(
            "http://media_service:80/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"c9979ad7-212c-4fbe-b2ce-c29dffa3dba4"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
