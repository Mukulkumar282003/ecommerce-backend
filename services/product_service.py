
from sqlalchemy.orm import Session
from models.product import Product
from schemas.product import ProductCreate,ProductResponse,ProductUpdate
from repositories.product_repository import(
      get_all_products,
      get_product_by_id,
      create_product as create_product_repository,
      update_product as update_product_repository,
      delete_product as delete_product_repository
)


def create_product(
    db:Session,
    product_data:ProductCreate
):

    new_product=Product(
        name=product_data.name,
        price=product_data.price,
        category=product_data.category
    )
    return create_product_repository(db,new_product)

def get_products(
        db: Session,
        page: int = 1,
        limit: int = 10,
        category: str | None = None,
        search: str | None = None,
        sort: str | None = None
):    
        return get_all_products(
              db,
              page,
              limit,
              category,
              search,
              sort
        )    


def get_product(
        db:Session,
        product_id:int
):
        return get_product_by_id(db,product_id)


def update_product(
    db:Session,
    product_id:int,
    product_data:ProductUpdate,
):

    product=get_product_by_id(db,product_id)

    if product is None:
        return None
    
    product.name=product_data.name   
    product.price=product_data.price    
    product.category=product_data.category    
    

    return update_product_repository(db,product)

def delete_product(
    db:Session,
    product_id:int,
    
):

    product=get_product_by_id(db,product_id)

    if product is None: 
            return False
    
    delete_product_repository(db,product)

    return True