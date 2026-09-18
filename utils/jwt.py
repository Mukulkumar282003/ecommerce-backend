from jose import jwt 
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/".env",override=True)

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data:dict):
    token_data=data.copy()

    expire_time=datetime.utcnow()+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_data["exp"]=expire_time

    access_token=jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return access_token
    
