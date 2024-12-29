from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class role(Base):
    __tablename__="role"
    role_id=Column(Integer, primary_key=True, autoincrement=True)
    role_name=Column(String,nullable=False)

