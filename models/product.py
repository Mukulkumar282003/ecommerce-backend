from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.orm import relationship

from database import Base

class Product(Base):
    __tablename__="products"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    price=Column(Float)
    category=Column(String)

    image_url=Column(String,nullable=True)

    cart_items=relationship(
        "CartItem",
        back_populates="product"
    )