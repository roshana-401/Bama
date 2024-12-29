
from typing import Annotated
from sqlalchemy.orm import Session
from App.core.db.database import get_db_user
from fastapi import Depends,HTTPException,status

from App.domain.models.user import role

class RoleRepository:
    def __init__(self,db:Annotated[Session,Depends(get_db_user)]):
        self.db=db
        
    def get_role_Admin(self):
        rolee=self.db.query(role).filter(role.role_name=="Admin")
        if not rolee.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=" مقام ادمین موجود نیست")
        
        return rolee.first().role_id
        
