
from typing import Annotated
from sqlalchemy.orm import Session
from ...core.db.database import get_db
from fastapi import Depends,HTTPException,status
from App.domain.models.user import users
from App.domain.schemas.user_schema import (
    GetPhoneNumber,
    GetPassword,
    UpdateUser,
    user_list
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
    
    def get_user_by_id(self,user_id:UUID):
        user=self.db.query(users).filter(users.user_id==user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="  چنین کاربری وجود ندارد")
        return user.first()
    
    def get_all_users(self):
        userss=self.db.query(users).all()
        return [user_list(date_register=str(user.date_register),date_update_Profile=str(user.date_update_Profile),status=str(user.status)
                          ,role='Admin' if user.role_id == 1 else 'User',phone_number=user.phone_number,user_id=user.user_id) for user in userss]
        
    
    def delete_user(self,user_id:UUID):
        user=self.db.query(users).filter(users.user_id==user_id)
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
    
    def update_Password_user(self,user_id:UUID,NewDetail:str):
        updated_user=self.db.query(users).filter(users.user_id==user_id)
        if not updated_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"کاربری با این شماره تلفن موجود نیست")
        
        updated_user.update({"password":NewDetail},synchronize_session=False)
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
        