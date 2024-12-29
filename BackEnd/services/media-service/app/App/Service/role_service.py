from typing import Annotated
from fastapi import Depends, HTTPException, status
from App.infrastructure.repositories.role_repository import RoleRepository

class RoleService:
    def __init__(
        self,
        role_repository: Annotated[RoleRepository, Depends()],
    ) -> None:
        super().__init__()

        self.role_repository = role_repository
        
    async def get_role_admin(self):
        role=self.role_repository.get_role_Admin()
        return role