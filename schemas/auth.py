from pydantic import BaseModel, HttpUrl
from typing import Optional




class GoogleUser(BaseModel):
    email: str
    name: Optional[str] = None
    image: Optional[HttpUrl] = None


class MetaAdAccountCreate(BaseModel):
    user_id: int
    fb_account_id: str
    name: str
    currency: str
    timezone: str
    access_token: str

class AdScoreCreate(BaseModel):
    fb_account_id: str
    score: float
    explanation: str
    recommendations: str