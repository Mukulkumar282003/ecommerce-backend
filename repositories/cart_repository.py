from sqlalchemy.orm import Session

from models.cart import Cart,CartItem


def get_cart_by_user(
    db: Session,
    user_id: int
):
    return db.query(Cart).filter(
        Cart.user_id == user_id
    ).first()


def create_cart(
    db: Session,
    cart: Cart
):
    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart

def get_cart_item(
    db: Session,
    cart_id: int,
    product_id: int
):
    return db.query(CartItem).filter(
        CartItem.cart_id == cart_id,
        CartItem.product_id == product_id
    ).first()


def create_cart_item(
    db: Session,
    cart_item: CartItem
):
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

def get_cart_items(
        db:Session,
        cart_id:int
):
    return db.query(CartItem).filter(CartItem.cart_id==cart_id).all()

def delete_cart_item(
        db:Session,
        cart_item:CartItem
):
    db.delete(cart_item)
    db.commit()

    return True

def update_cart_item(
        db:Session,
        cart_item:CartItem
):
    db.commit()
    db.refresh(cart_item)

    return cart_item

def clear_cart(
        db:Session,
        cart_id:int
):
    
    db.query(CartItem).filter(CartItem.cart_id==cart_id).delete()

    db.commit()

    return True