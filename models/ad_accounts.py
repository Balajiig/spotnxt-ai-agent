from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, Float
from db.base import Base
from sqlalchemy.sql import func, text



class MetaAdAccount(Base):
    __tablename__ = "meta_ad_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fb_account_id = Column(String(50), unique=True, nullable=False)
    name = Column(Text)
    currency = Column(Text)
    timezone = Column(Text)
    access_token = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('Asia/Kolkata', now())"))

class AdScore(Base):
    __tablename__ = "ad_scores"
    id = Column(Integer, primary_key=True, index=True)
    fb_account_id = Column(String(50), ForeignKey("meta_ad_accounts.fb_account_id"))
    score = Column(Float)
    explanation = Column(Text)
    recommendations = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('Asia/Kolkata', now())"))
