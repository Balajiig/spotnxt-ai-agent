from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import text
from db.base import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(TIMESTAMP(timezone=True),server_default=text("TIMEZONE('Asia/Kolkata', CURRENT_TIMESTAMP)"))
