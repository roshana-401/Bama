import random
from typing import Annotated
from fastapi import Depends
from redis import Redis

from App.core.redis.redis import get_redis_client
from ..base_service import BaseService


class OTPService(BaseService):
    def __init__(
        self, redis_client: Annotated[Redis, Depends(get_redis_client)]
    ) -> None:
        super().__init__()
        self.redis_client = redis_client

    @staticmethod
    def __generate_otp() -> str:
        return str(random.randint(100000, 999999))

    def send_otp(self, phone_number: str):
        otp = self.__generate_otp()        
        self.redis_client.setex(phone_number, self.config.otp_expire_time, otp)
        print({"OTP Code":otp})

    def verify_otp(self, phone_number: str, otp: str) -> bool:
        stored_otp = self.redis_client.get(phone_number)
        return stored_otp is not None and stored_otp == otp

    def check_exist(self, phone_number: str) -> bool:
        stored_otp = self.redis_client.get(phone_number)
        return stored_otp is not None
