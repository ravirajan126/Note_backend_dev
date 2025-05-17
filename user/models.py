import uuid
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_name = Column(String(100))
    user_email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_on = Column(DateTime, default=datetime.utcnow)
