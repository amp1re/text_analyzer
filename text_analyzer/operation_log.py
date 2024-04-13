from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from database import Base


class OperationLog(Base):
    __tablename__ = "operation_log"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="operations")
    text = Column(String)
    status = Column(String)
    result = Column(JSON)
    cost_of_operation = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
