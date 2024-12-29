import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status
import asyncio
import httpx



async def get_mock_phoneNumber():
    import random
    rand=str(random.randint(1000, 9999))
    return f"0911786{rand}"


@pytest.mark.asyncio
async def test_initialize_register():
    async with httpx.AsyncClient() as client:

        phone = await get_mock_phoneNumber()
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_409_CONFLICT



@pytest.mark.asyncio
async def test_finalize_register():
    async with httpx.AsyncClient() as client:
        phone = await get_mock_phoneNumber()

        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK


        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_request_otp():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK
        
        otp = input("Enter OTP: ")

        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_verify_otp():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK


        
        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_wrong_otp():
    import random
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        #wrong OTP
        code=str(random.randint(100000, 999999))
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":code})
        assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.asyncio
async def test_wrong_phoneNumber_in_step_two():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK


        phone = await get_mock_phoneNumber()
        #wrong OTP
        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.asyncio
async def test_wrong_PhoneNumber_inStepThree():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        
        phone = await get_mock_phoneNumber()

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_resend_otp_wrong():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK
        
        response = await client.post("http://iam_service:80/user/Sign/ResendToken", json={"phone_number": phone})
        assert response.status_code == status.HTTP_208_ALREADY_REPORTED

@pytest.mark.asyncio
async def test_resend_otp_true():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK
        
        await asyncio.sleep(60)
        
        response = await client.post("http://iam_service:80/user/Sign/ResendToken", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_resend_otp_Not_exist_PhoneNumber():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/ResendToken", json={"phone_number": phone})
        assert response.status_code == status.HTTP_404_NOT_FOUND


    
@pytest.mark.asyncio
async def test_resend_otp_after_register():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post("http://iam_service:80/user/Sign/ResendToken", json={"phone_number": phone})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
@pytest.mark.asyncio
async def test_Login():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post("http://iam_service:80/user/Login", data={"username": phone,"password":"12345678"})
        assert response.status_code == status.HTTP_200_OK
    
    
@pytest.mark.asyncio
async def test_Login_with_wrong_phoneNumber():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Login", data={"username": phone,"password":"12345678"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
    
    
@pytest.mark.asyncio
async def test_Login_with_wrong_password():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.post("http://iam_service:80/user/Login", data={"username": phone,"password":"12345670"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
@pytest.mark.asyncio
async def test_token():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED
        
        response = await client.get("http://iam_service:80/TokenVerify",headers={"Authorization": f"Bearer {response.json().get('Token')}"})
        assert response.status_code == status.HTTP_200_OK
        
        response = await client.post("http://iam_service:80/user/Login", data={"username": phone,"password":"12345678"})
        assert response.status_code == status.HTTP_200_OK
        
        response = await client.get("http://iam_service:80/TokenVerify",headers={"Authorization": f"Bearer {response.json().get('Token')}"})
        assert response.status_code == status.HTTP_200_OK
        
    
@pytest.mark.asyncio
async def test_Wrong_token():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED
        
        tokenWrong=response.json().get('Token')
        tokenWrong+="000"
        
        response = await client.get("http://iam_service:80/TokenVerify",headers={"Authorization": f"Bearer {tokenWrong}"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_expire_token():
    phone = await get_mock_phoneNumber()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://iam_service:80/user/Sign/SendVerifyMessage", json={"phone_number": phone})
        assert response.status_code == status.HTTP_200_OK

        otp = input("Enter OTP: ")
        response = await client.post("http://iam_service:80/user/Sign/VerifyMessage", json={"phone_number": phone,"OTP":otp})
        assert response.status_code == status.HTTP_200_OK

        response = await client.post("http://iam_service:80/user/Sign/Register", json={"phone_number": phone, "password": "12345678"})
        assert response.status_code == status.HTTP_201_CREATED
        
        await asyncio.sleep(60)
        
        response = await client.get("http://iam_service:80/TokenVerify",headers={"Authorization": f"Bearer {response.json().get('Token')}"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

