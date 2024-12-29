
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import (get_db_user)
from fastapi import Depends,HTTPException,status
from sqlalchemy.dialects.postgresql import UUID
from App.domain.models.user import users
class UserRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db_user)]):
        self.db=db
        
    def get_user_by_id(self,user_id:UUID):
        user=self.db.query(users).filter(users.user_id==user_id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="  چنین کاربری وجود ندارد")
        return user.first()
        
        
   