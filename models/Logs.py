from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String, index=True)
