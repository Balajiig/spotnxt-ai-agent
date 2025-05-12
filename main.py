from fastapi import FastAPI
from db.session import engine
from db.base import Base
from api.routes import auth
import models.user
import models.payment
import models.chat_history
import models.ad_accounts

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth.router, prefix="/api")


