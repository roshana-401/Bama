from sqlalchemy import Column, String, TIMESTAMP, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from .operation_status import OperationStatus
from ...core.db.database import get_Base_Class
from App.domain.models.user import users
from App.domain.models.sell_spare_part import SellSpareParts

Base=get_Base_Class()

class saveSellSparePart(Base):
    __tablename__="saveSparePart"
    user_id = Column(UUID(as_uuid=True),ForeignKey(users.user_id,ondelete="CASCADE"),primary_key=True, nullable=False)
    sell_spare_parts_id=Column(UUID(as_uuid=True),ForeignKey(SellSpareParts.sell_spare_parts_id,ondelete="CASCADE"),primary_key=True,nullable=False)
