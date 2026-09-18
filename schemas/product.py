from pydantic import BaseModel,Field

class ProductCreate(BaseModel):
    name:str=Field(min_length=2)
    price:float=Field(gt=0)
    category:str=Field(min_length=2)

class ProductUpdate(BaseModel):
    name:str=Field(min_length=2)
    price:float=Field(gt=0)
    category:str

class ProductResponse(BaseModel):
    id:int
    name:str
    price:float
    category:str
    image_url:str|None=None

    class Config:
        from_attributes=True
