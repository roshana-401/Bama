import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status
import asyncio
from io import BytesIO
from App.main import app
from fastapi.testclient import TestClient
import httpx
from asyncio import get_event_loop
async def get_mock_phoneNumber():
    import random
    rand=str(random.randint(1000, 9999))
    return f"0911786{rand}"

def open_image_file(path: str):
    with open(path, 'rb') as f:
        files = {'file': ('file.jpg', f)}
        return files


token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzU4NzQxMGMtZjZkOC00NTMwLWEyNWItMjY5OGI3N2U1ZDk0Iiwicm9sZV9pZCI6Miwic3RhdGUiOiJhY3RpdmUiLCJleHAiOjE3MzUxNTExMDR9.Lz4YQJL8egap0EQdOjxRvEGTcC9oAINNAU0uNq1CXbc"


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        yield client

@pytest.mark.asyncio
async def test_get_Wrong_media_car(client):
    response = await client.post(
        "/Media/Car/GetMediaCar",
        json={"mongo_id": "676c1226f69bcb10c217432b"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_Wrong_media_spare_part(client):
    response = await client.post(
        "/Media/SpareParts/GetMediaSparePart",
        json={"mongo_id": "676c2fe82a191a9c1f96a839"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

# @pytest.mark.asyncio
# async def test_get_Wrong_user_media_car(client):
#     response =await client.post(
#         "/Media/Car/GetMediaCar",
#         json={"mongo_id":"676c1226f69bcb10c217432b"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
# @pytest.mark.asyncio
# async def test_get_Wrong_user_media_spare(client):
#     response =await client.post(
#         "/Media/SpareParts/GetMediaSparePart",
#         json={"mongo_id":"676c1226f69bcb10c217432b"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
# @pytest.mark.asyncio
# async def test_delete_Wrong_media(client):
    
#     response =await client.delete(
#         "/Media/Car/DeleteMediaCar",
#         json={"mongo_id":"676c03df5bae3e48402e0das"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_404_NOT_FOUND

#     response =await client.delete(
#         "/Media/SpareParts/DeleteMediaSparePart",
#         json={"mongo_id":"676c03df5bae3e48402e0das"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# @pytest.mark.asyncio
# async def test_delete_Wrong_user_media(client):
#     response =await client.delete(
#         "/Media/Car/DeleteMediaCar",
#         json={"mongo_id":"676c1226f69bcb10c217432b"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN

#     response =await client.delete(
#         "/Media/SpareParts/DeleteMediaSparePart",
#         json={"mongo_id":"676c1226f69bcb10c217432b"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN

# @pytest.mark.asyncio
# async def test_get_all_Wrong_media(client):
    
#     response =await client.post(
#         "/Media/Car/GetAllMediaIdCar",
#         json={"sell_car_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f661"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_404_NOT_FOUND

#     response =await client.post(
#         "/Media/SpareParts/GetAllMediaIdSpareParts",
#         json={"sell_spareparts_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f661"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# @pytest.mark.asyncio
# async def test_get_all_Wrong_user_media(client):
#     response =await client.post(
#         "/Media/Car/GetAllMediaIdCar",
#         json={"sell_car_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN

#     response =await client.post(
#         "/Media/SpareParts/GetAllMediaIdSpareParts",
#         json={"sell_spareparts_id":"1ff54ecb-4c80-4857-8ac2-5a39fa54f667"},  
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
#     assert response.status_code == status.HTTP_403_FORBIDDEN
