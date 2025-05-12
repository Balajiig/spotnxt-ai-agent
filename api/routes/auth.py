from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.auth import  GoogleUser
from google.oauth2 import id_token
import os
from dotenv import load_dotenv
import httpx
from fastapi.responses import RedirectResponse
from models.user import User
from models.ad_accounts import MetaAdAccount
from db.session import sessionmaker
from jose import jwt




router = APIRouter()


load_dotenv()  # Load environment variables from .env



@router.post("/users/google-login")
async def google_login(user: GoogleUser, db: Session = Depends(get_db)):
    print("Received user data:", user.dict())

    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        new_user = User(
            email=user.email,
            full_name=user.name,
            image=str(user.image) if user.image else None,
            oauth_provider="google"
        )
        db.add(new_user)
    else:
        existing_user.full_name = user.name
        existing_user.image = str(user.image) if user.image else None

    db.commit()
    return {"status": "ok"}

    
FB_CLIENT_ID = os.getenv("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET")
FB_REDIRECT_URI = os.getenv("FB_REDIRECT_URI")

@router.get("/auth/meta/callback")
async def auth_callback(code: str, db: Session = Depends(get_db), user_id: int = 1):  # Replace `user_id` logic appropriately
    # 1. Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_resp = await client.get("https://graph.facebook.com/v17.0/oauth/access_token", params={
            "client_id": FB_CLIENT_ID,
            "client_secret": FB_CLIENT_SECRET,
            "redirect_uri": FB_REDIRECT_URI,
            "code": code,
        })

    token_data = token_resp.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to get access token")

    # 2. Fetch /me/adaccounts using access token
    async with httpx.AsyncClient() as client:
        ad_accounts_resp = await client.get(
            "https://graph.facebook.com/v17.0/me/adaccounts",
            params={"access_token": access_token}
        )

    ad_data = ad_accounts_resp.json()
    accounts = ad_data.get("data", [])

    # 3. Store each account in the meta_ad_accounts table
    stored_accounts = []
    for acc in accounts:
        fb_account_id = acc.get("id")
        name = acc.get("name", "")
        currency = acc.get("currency", "")
        timezone = acc.get("timezone_name", "")

        # Check if account already exists
        existing = db.query(MetaAdAccount).filter_by(fb_account_id=fb_account_id).first()
        if not existing:
            new_account = MetaAdAccount(
                user_id=user_id,
                fb_account_id=fb_account_id,
                name=name,
                currency=currency,
                timezone=timezone,
                access_token=access_token
            )
            db.add(new_account)
            stored_accounts.append(fb_account_id)

    db.commit()
    return {
        "message": "Meta ad accounts stored successfully.",
        "stored_accounts": stored_accounts,
        "total_accounts": len(stored_accounts)
    }

    

@router.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users