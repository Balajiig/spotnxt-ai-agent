import os
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy.orm import sessionmaker  # ✅ this fixes your issue
import pg8000
from dotenv import load_dotenv

load_dotenv()

# Load env vars
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Initialize connector
connector = Connector()

def getconn():
    return connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )

# Create SQLAlchemy engine
engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
)

# Use correct import here
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
