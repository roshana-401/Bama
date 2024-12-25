from ...core.db.database import get_Base_Class
from sqlalchemy import Column,Integer,String,ForeignKey,func

Base=get_Base_Class()

class role(Base):
    __tablename__="role"
    role_id=Column(Integer, primary_key=True, autoincrement=True)
    role_name=Column(String,nullable=False)