import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Note(Base):
    __tablename__ = "notes"
    note_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_title = Column(String(255))
    note_content = Column(String(1000))
    user_id = Column(String(36), ForeignKey("users.user_id"))
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_on = Column(DateTime, default=datetime.utcnow)