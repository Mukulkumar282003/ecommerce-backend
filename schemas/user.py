from pydantic import BaseModel,Field,EmailStr

class UserCreate(BaseModel):
    username:str=Field(min_length=3)
    email:EmailStr   
    password:str=Field(min_length=6)

class UserResponse(BaseModel):
    id:int
    username:str
    email:str

    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str
