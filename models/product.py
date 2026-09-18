from sqlalchemy import create_engine,Column,Integer,String,Float

from database import Base

class Product(Base):
    __tablename__="products"
    
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    price=Column(Float)
    category=Column(String)

    image_url=Column(String,nullable=True)