from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate,UserLogin
from utils.security import hash_password,verify_password
from utils.jwt import create_access_token
from repositories.user_repository import (
    get_user_by_email,
    create_user
)

def register_user(db:Session,user_data:UserCreate):
    existing_user=get_user_by_email(db,user_data.email)
    if existing_user:
        return None

    new_user=User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    return create_user(db,new_user)

def login_user(db:Session,user_data:UserLogin):
    user=get_user_by_email(
        db,
        user_data.email
    )
    
    if user is None:
        return None

    password_correct=verify_password(
        user_data.password,
        user.password
    )

    if not password_correct:
        return None
    
    print("LOGIN USER:",user.username)
    print("LOGIN EMAIL:",user.email)
    print("LOGIN ROLE:",user.role)
    access_token=create_access_token(
        {
            "user_id":user.id,
            "email":user.email,
            "role":user.role
        }
    )

    return{ 
        "access_token":access_token,
        "token_type":"bearer"
    }    