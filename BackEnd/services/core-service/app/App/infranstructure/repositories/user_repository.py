
from typing import Annotated
from sqlalchemy.orm import Session
from ...core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.models.user import users
from App.domain.schemas.user_schema import (
    GetPhoneNumber,
    UpdatePasswordUser,
    UpdateUser,
)
from App.domain.models.user_status import UserStatus
from sqlalchemy.dialects.postgresql import UUID

class UserRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db)]):
        self.db=db
        
    def create_user(self,user:users):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    
    def delete_user(self,user:users):
        user.delete(synchronize_session=False)
        self.db.commit()
    
    def update_State_user(self,user_id:UUID):
        updated_user=self.db.query(users).filter(users.user_id==user_id)
        if not updated_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"کاربری با این شماره تلفن موجود نیست")
        updated_user.update({"status":UserStatus.verified},synchronize_session=False)
        self.db.commit()
        
        return updated_user.first()
    
    def update_PhoneNumber_user(self,user_id:UUID,NewDetail:UpdateUser):
        updated_user=self.db.query(users).filter(users.user_id==user_id)
        if not updated_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"کاربری با این شماره تلفن موجود نیست")
        
        updated_user.update({"phone_number":NewDetail.phone_number},synchronize_session=False)
        self.db.commit()
        
        return updated_user.first()
    
    def update_Password_user(self,user_id:UUID,NewDetail:UpdatePasswordUser):
        updated_user=self.db.query(users).filter(users.user_id==user_id)
        if not updated_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"کاربری با این شماره تلفن موجود نیست")
        
        updated_user.update({"password":NewDetail.password},synchronize_session=False)
        self.db.commit()
        
        return updated_user.first()
    
    def update_user_StepThree(self,user_id:UUID,user:users):
        updated_user=self.db.query(users).filter(users.user_id==user_id)
        if not updated_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"کاربری با این شماره تلفن موجود نیست")
        
        updated_user.update({"password":user.password,"role_id":user.role_id,"status":user.status},synchronize_session=False)
        self.db.commit()
        return updated_user.first()

    def get_user(self, user_id: UUID):
        
        return self.db.get(users, user_id)

    def get_user_with_PhoneNumber(self, detail: GetPhoneNumber):
        
        user=self.db.query(users).filter(users.phone_number==detail.phone_number)
        return user.first()
        