from sqlalchemy.orm import Session

from models.order import Order
from models.product import Product

from repositories.order_repository import (
    create_order,
    get_orders_by_user,
    get_order_by_id,
    update_order_status,
    get_all_orders
)

from repositories.cart_repository import (
    get_cart_by_user,
    get_cart_items,
    clear_cart
)


def place_order(
    db: Session,
    user_id: int
):
    cart = get_cart_by_user(
        db,
        user_id
    )

    if cart is None:
        return None

    cart_items = get_cart_items(
        db,
        cart.id
    )

    if not cart_items:
        return None

    total_amount = 0

    for item in cart_items:

        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if product is None:
            return None

        total_amount += (
            product.price * item.quantity
        )

    new_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )

    order=create_order(db,new_order)

    clear_cart(db,cart.id)

    return order


def get_my_orders(
    db: Session,
    user_id: int
):
    return get_orders_by_user(
        db,
        user_id
    )


def get_order(
    db: Session,
    order_id: int
):
    return get_order_by_id(
        db,
        order_id
    )


def change_order_status(
        db:Session,
        order_id:int,
        status:str
):
    order=get_order_by_id(db,order_id)

    if order is None:
        return None

    return update_order_status(db,order,status)

def get_all_orders_for_admin(
        db:Session
):
    return get_all_orders(db)