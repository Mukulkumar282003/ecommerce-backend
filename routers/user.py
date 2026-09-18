from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from schemas.user import UserCreate,UserResponse,UserLogin,Token
from services.user_service import register_user,login_user

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register",response_model=UserResponse)
def register(
    user_data:UserCreate,
    db=Depends(get_db)
):

    user=register_user(db,user_data)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="email already registered"
        )        
    return user

@router.post("/login",response_model=Token)
def login(
    user_data:UserLogin,
    db=Depends(get_db)
):
    user =login_user(
        db,
        user_data
    )
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="invalid email or password"
        )

    return user
    