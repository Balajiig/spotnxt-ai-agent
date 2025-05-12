from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from db.base import Base
from sqlalchemy.sql import text

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    status = Column(String, default="pending")  # or success, failed
    payment_provider = Column(String)  # Razorpay, Stripe, etc.
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('Asia/Kolkata', now())"))
