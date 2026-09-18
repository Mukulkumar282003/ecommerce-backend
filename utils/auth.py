from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from utils.jwt import SECRET_KEY, ALGORITHM
from database import get_db
from models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),db=Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id=payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="invalid token"
            )
        
        user=db.query(User).filter(User.id==user_id).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="user not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
def require_admin(current_user=Depends(get_current_user)):
    print("USER ROLE:",current_user.role)
    
    if current_user.role !="admin":
        raise HTTPException(
            status_code=403,
            detail="admin access required"
        )
    
    return current_user


    