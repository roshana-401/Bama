import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status
import asyncio

from app.App.main import app



async def get_mock_phoneNumber():
    import random
    rand=str(random.randint(1000, 9999))
    return f"0911786{rand}"

@pytest_asyncio.fixture(autouse=True)
async def client():
    async with AsyncClient(app=app, base_url="http://iam.localhost") as ac:
    # async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.mark.asyncio
async def test_initialize_register(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_409_CONFLICT



@pytest.mark.asyncio
async def test_finalize_register(client):
    phone = await get_mock_phoneNumber()

    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK


    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_request_otp(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK
    
    otp = input("Enter OTP: ")

    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_verify_otp(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK


    
    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_wrong_otp(client):
    import random
    phone = await get_mock_phoneNumber()

    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    #wrong OTP
    code=str(random.randint(100000, 999999))
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":code})
    assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.asyncio
async def test_wrong_phoneNumber_in_step_two(client):
    phone = await get_mock_phoneNumber()

    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK


    phone = await get_mock_phoneNumber()
    #wrong OTP
    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.asyncio
async def test_wrong_PhoneNumber_inStepThree(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    
    phone = await get_mock_phoneNumber()

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_resend_otp_wrong(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK
    
    response = await client.post("/user/Sign/ResendToken", json={"phone_number": phone})
    assert response.status_code == status.HTTP_208_ALREADY_REPORTED

@pytest.mark.asyncio
async def test_resend_otp_true(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK
    
    await asyncio.sleep(60)
    
    response = await client.post("/user/Sign/ResendToken", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_resend_otp_Not_exist_PhoneNumber(client):
    phone = await get_mock_phoneNumber()
    
    response = await client.post("/user/Sign/ResendToken", json={"phone_number": phone})
    assert response.status_code == status.HTTP_404_NOT_FOUND


    
@pytest.mark.asyncio
async def test_resend_otp_after_register(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED
    
    response = await client.post("/user/Sign/ResendToken", json={"phone_number": phone})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.asyncio
async def test_Login(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED
    
    response = await client.post("/user/Login", json={"phone_number": phone,"password":"12345678"})
    assert response.status_code == status.HTTP_200_OK
    
    
@pytest.mark.asyncio
async def test_Login_with_wrong_phoneNumber(client):
    phone = await get_mock_phoneNumber()
    
    response = await client.post("/user/Login", json={"phone_number": phone,"password":"12345678"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    
@pytest.mark.asyncio
async def test_Login_with_wrong_password(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED
    
    response = await client.post("/user/Login", json={"phone_number": phone,"password":"12345670"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
@pytest.mark.asyncio
async def test_token(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED
    
    response = await client.get("/TokenVerify",headers={"Authorization": f"Bearer {response.json().get('Token')}"})
    assert response.status_code == status.HTTP_200_OK
    
    response = await client.post("/user/Login", json={"phone_number": phone,"password":"12345678"})
    assert response.status_code == status.HTTP_200_OK
    
    response = await client.get("/TokenVerify",headers={"Authorization": f"Bearer {response.json().get('Token')}"})
    assert response.status_code == status.HTTP_200_OK
    
    
@pytest.mark.asyncio
async def test_Wrong_token(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED
    
    tokenWrong=response.json().get('Token')
    tokenWrong+="000"
    
    response = await client.get("/TokenVerify",headers={"Authorization": f"Bearer {tokenWrong}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_expire_token(client):
    phone = await get_mock_phoneNumber()
    response = await client.post("/user/Sign/SendVerifyMessage", json={"phone_number": phone})
    assert response.status_code == status.HTTP_200_OK

    otp = input("Enter OTP: ")
    response = await client.post("/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
    assert response.status_code == status.HTTP_201_CREATED
    
    await asyncio.sleep(60)
    
    response = await client.get("/TokenVerify",headers={"Authorization": f"Bearer {response.json().get('Token')}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

