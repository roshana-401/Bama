from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text

from ...core.db.database import get_Base_Class
from .user_status import UserStatus
Base=get_Base_Class()

class role(Base):
    __tablename__="role"
    role_id=Column(Integer, primary_key=True, autoincrement=True)
    role_name=Column(String,nullable=False)

class users(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True),primary_key=True,nullable=False,server_default=text("gen_random_uuid()"))
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_register = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    status = Column(Enum(UserStatus), nullable=False)
    date_update_Profile = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=False)
