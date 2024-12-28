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
            "http://media.localhost/Media/Car/GetMediaCar",
            json={"mongo_id": "676c1226f69bcb10c217432b"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    

@pytest.mark.asyncio
async def test_get_Wrong_media_spare_part():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media.localhost/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id": "676c2fe82a191a9c1f96a839"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_Wrong_user_media_car():
    token=await get_token()
    async with httpx.AsyncClient() as client:
        response =await client.post(
            "http://media.localhost/Media/Car/GetMediaCar",
            json={"mongo_id":"676f4c6a836b7dc2e48d3d95"},  
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
            "http://media.localhost/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id":"676f4c9a836b7dc2e48d3d98"},  
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
            "http://media.localhost/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id":"676f4e36b30acdd86eb2ac6e"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        response =await client.post(
            "http://media.localhost/Media/Car/GetMediaCar",
            json={"mongo_id":"676f4e7fb30acdd86eb2ac73"},  
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
            "http://media.localhost/Media/SpareParts/GetMediaSparePart",
            json={"mongo_id":"676f4e36b30acdd86eb2ac6e"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        response =await client.post(
            "http://media.localhost/Media/Car/GetMediaCar",
            json={"mongo_id":"676f4e7fb30acdd86eb2ac73"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK

#--------------------------------------------------add
#wrong user add to wrong sell_car or sell_sparePart
#--------------------------------------------------

@pytest.mark.asyncio
async def test_upload_Wrong_media_size_spare_part():
    token=await get_token()
    file=await open_image_file("file2.jpg")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://media.localhost/Media/SpareParts/UploadMediaSparePart",
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
            "http://media.localhost/Media/Car/UploadMediaCar",
            files={"file":("file2.jpg", file,"image/jpg")},  
            data={"car_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
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
            "http://media.localhost/Media/SpareParts/UploadMediaSparePart",
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
            "http://media.localhost/Media/Car/UploadMediaCar",
            files={"file":("character.mp3", file,"file/mp3")},  
            data={"car_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
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
            "http://media.localhost/Media/Car/DeleteMediaCar",
            params={"mongo_id":"676c1226f69bcb10c217432b"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response =await client.delete(
            "http://media.localhost/Media/SpareParts/DeleteMediaSparePart",
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
            "http://media.localhost/Media/Car/DeleteMediaCar",
            params={"mongo_id":"676f4d47836b7dc2e48d3da5"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response =await client.delete(
            "http://media.localhost/Media/SpareParts/DeleteMediaSparePart",
            params={"mongo_id":"676f4d5b836b7dc2e48d3da8"},  
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
            "http://media.localhost/Media/Car/UploadMediaCar",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"car_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]

        response =await client.delete(
            "http://media.localhost/Media/Car/DeleteMediaCar",
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
            "http://media.localhost/Media/Car/UploadMediaCar",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"car_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]

        response =await client.delete(
            "http://media.localhost/Media/Car/DeleteMediaCar",
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
            "http://media.localhost/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]
        
        response =await client.delete(
            "http://media.localhost/Media/SpareParts/DeleteMediaSparePart",
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
            "http://media.localhost/Media/SpareParts/UploadMediaSparePart",
            files={"file":("file.jpg", file,"image/jpg")},  
            data={"spare_part_sell_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        result=response.json()
        result=result["mongo_id"]
        
        response =await client.delete(
            "http://media.localhost/Media/SpareParts/DeleteMediaSparePart",
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
            "http://media.localhost/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f661"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response =await client.post(
            "http://media.localhost/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f661"},  
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
            "http://media.localhost/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f668"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK

        response =await client.post(
            "http://media.localhost/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f668"},  
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
            "http://media.localhost/Media/Car/GetAllMediaIdCar",
            json={"sell_car_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f668"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK

        response =await client.post(
            "http://media.localhost/Media/SpareParts/GetAllMediaIdSpareParts",
            json={"sell_spareparts_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f668"},  
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == status.HTTP_200_OK
