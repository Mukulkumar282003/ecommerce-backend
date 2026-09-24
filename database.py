from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker 



DATABASE_URL="sqlite:///./ecommerce.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}

)
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base=declarative_base()

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

from models.product import Product
from models.user import User    
from models.cart import Cart,CartItem    
from models.order import Order

Base.metadata.create_all(bind=engine)