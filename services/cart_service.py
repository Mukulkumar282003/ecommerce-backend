from sqlalchemy.orm import Session 

from models.product import Product

from models.cart import Cart, CartItem

from repositories.cart_repository import (
    get_cart_by_user,
    create_cart,
    get_cart_item,
    create_cart_item,
    delete_cart_item,
    update_cart_item
)


def add_to_cart(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int
):

    product=db.query(Product).filter(Product.id==product_id).first()

    if product is  None:
        return None
    
    cart = get_cart_by_user(
        db,
        user_id
    )

    if cart is None:
        cart = Cart(
            user_id=user_id
        )

        cart = create_cart(
            db,
            cart
        )

    existing_item = get_cart_item(
        db,
        cart.id,
        product_id
    )

    if existing_item:
        existing_item.quantity += quantity

        db.commit()
        db.refresh(existing_item)

        return existing_item

    new_item = CartItem(
        cart_id=cart.id,
        product_id=product_id,
        quantity=quantity
    )

    return create_cart_item(
        db,
        new_item
    )


def get_my_cart(
    db: Session,
    user_id: int
):
    cart = get_cart_by_user(
        db,
        user_id
    )

    if cart is None:
        return []

    return cart.items


def remove_from_cart(
    db: Session,
    user_id: int,
    product_id: int
):
    cart = get_cart_by_user(
        db,
        user_id
    )

    if cart is None:
        return False

    cart_item = get_cart_item(
        db,
        cart.id,
        product_id
    )

    if cart_item is None:
        return False

    delete_cart_item(
        db,
        cart_item
    )

    return True

def update_cart_quantity(
        db:Session,
        user_id:int,
        product_id:int,
        quantity:int
):
    cart=get_cart_by_user(db,user_id)

    if cart is None:
        return None

    cart_item=get_cart_item(db,cart.id,product_id)

    if cart_item is None:
        return None

    cart_item.quantity=quantity

    return update_cart_item(db,cart_item)
