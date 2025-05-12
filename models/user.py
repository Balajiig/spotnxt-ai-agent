from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.sql import text
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)  
    image = Column(String, nullable=True)     
    date_of_birth = Column(String, nullable=True)   
    
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    oauth_provider = Column(String, nullable=True)  # e.g., "google", "meta"
    oauth_id = Column(String, unique=True, nullable=True)  # e.g., Google sub or Meta user ID

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('Asia/Kolkata', now())"))

    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('Asia/Kolkata', now())"))



