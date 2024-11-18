from typing import Annotated
from uuid import UUID
from fastapi import Depends

from ..domain.models.user import users
from ..infranstructure.repositories.user_repository import UserRepository
from .auth_service.hash_service import HashService
from ..domain.schemas.user_schema import (
    UpdateUser ,
    CreateUser,
    GetPhoneNumber,
    CreateUserStepThree

)
    
from .auth_service.hash_service import HashService
from .base_service import BaseService

class UserService(BaseService):
    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends()],
        hash_service: Annotated[HashService, Depends()],
    ) -> None:
        super().__init__()
        self.user_repository = user_repository
        self.hash_service = hash_service

    async def create_user(self, createUser: CreateUserStepThree):
        user=users(
            phone_number=createUser.phone_number,
            password=self.hash_service.hash(createUser.password),
            role_id=2,
            status="active"
        )
        return self.user_repository.create_user(user)
    
    async def create_user_stepOne(self, createUser: CreateUser):
        user=users(
            phone_number=createUser.phone_number,
            status="unverified"
        )
        return self.user_repository.create_user(user)

    async def update_PhoneNumber_user(self, user_id: UUID, newDetail: UpdateUser):

        return self.user_repository.update_PhoneNumber_user(user_id, newDetail)
    
    async def update_user_RegisterStepThree(self, user_id: UUID, newDetail: CreateUserStepThree):
        user=users(
            phone_number=newDetail.phone_number,
            password=self.hash_service.hash(newDetail.password),
            role_id=2,
            status="active"
        )
        return self.user_repository.update_user_StepThree(user_id=user_id,user=user)
    
    async def update_State_user(self, user_id: UUID):

        return self.user_repository.update_State_user(user_id)

    async def delete_user(self, user: users) -> None:
        
        return self.user_repository.delete_user(user)

    async def get_user(self, user_id: UUID):
        return self.user_repository.get_user(user_id)

    async def get_user_with_phone_number(self, phone_number:GetPhoneNumber):
        return self.user_repository.get_user_with_PhoneNumber(phone_number)
