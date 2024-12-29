import pytest
import pytest_asyncio
from fastapi import status
from App.main import app
import httpx


    
async def get_token2():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://iam_service:80/user/Login",
            data={"username": "09117865508", "password": "123456213"}
        )
        response_data = response.json()
        return response_data["Token"]
    

@pytest.mark.asyncio
async def test_Add_dublicate_carCompony():
    token=await get_token2()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://core_service:80/admin/carCompony/Add",
            json={"car_compony_name": "ppprrpp"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post(
            "http://core_service:80/admin/carCompony/Add",
            json={"car_compony_name": "ppprrpp"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response = await client.delete(
            "http://core_service:80/admin/carCompony/delete",
            params={"car_compony_id": "7024ab01-9839-43f4-9666-53b5b70891cd"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    

@pytest.mark.asyncio
async def test_Add_dublicate_model():
    token=await get_token2()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://core_service:80/admin/modelCar/Add",
            json={"car_compony_id": "f75fc0bd-a289-4893-908f-ff4d715d52e8","model_car_name":"qqqqqq"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post(
            "http://core_service:80/admin/modelCar/Add",
            json={"car_compony_id": "f75fc0bd-a289-4893-908f-ff4d715d52e8","model_car_name":"qqqqqq"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response = await client.delete(
            "http://core_service:80/admin/modelCar/delete",
            params={"model_car_id": "94ec0173-86a6-4162-9c8e-c122c725e3f1"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_Add_dublicate_province():
    token=await get_token2()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://core_service:80/admin/province/Add",
            json={"province_name": "qqqqqqqqq"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post(
            "http://core_service:80/admin/province/Add",
            json={"province_name": "qqqqqqqqq"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response = await client.delete(
            "http://core_service:80/admin/province/delete",
            params={"province_id": "0c7b1f9e-08ab-4ae7-8c02-8e2cc2dd6e1c"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_Add_dublicate_city():
    token=await get_token2()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://core_service:80/admin/city/Add",
            json={"city_name": "qqqqwqwqq","province_id":"a17510f7-2d8f-41e8-80e9-1e14435ccfc9"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post(
            "http://core_service:80/admin/city/Add",
            json={"city_name": "qqqwqwqqqq","province_id":"a17510f7-2d8f-41e8-80e9-1e14435ccfc9"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        response = await client.delete(
            "http://core_service:80/admin/city/delete",
            params={"city_id": "2988a7d3-b444-410e-af66-9bd3e5385f62"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
