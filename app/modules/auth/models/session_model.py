# backend/models.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, func
from ....db.database import Base

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    data = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
