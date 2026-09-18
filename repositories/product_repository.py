from sqlalchemy.orm import Session
from models.product import Product


def get_all_products(
    db: Session,
    page: int = 1,
    limit: int = 10,
    category: str | None = None,
    search: str | None = None,
    sort: str | None = None
):
    query = db.query(Product)

    # Category filter
    if category:
        query = query.filter(
            Product.category == category
        )

    # Name search
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    # Sorting
    if sort == "price":
        query = query.order_by(
            Product.price
        )

    elif sort == "-price":
        query = query.order_by(
            Product.price.desc()
        )

    # Pagination
    offset = (page - 1) * limit

    products = query.offset(offset).limit(limit).all()

    return products


def get_product_by_id(
    db: Session,
    product_id: int
):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def create_product(
    db: Session,
    product: Product
):
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(
    db: Session,
    product: Product
):
    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product
):
    db.delete(product)
    db.commit()

    return True