from sqlalchemy.orm import Session

from models.order import Order


def create_order(
    db: Session,
    order: Order
):
    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_orders_by_user(
    db: Session,
    user_id: int
):
    return db.query(Order).filter(
        Order.user_id == user_id
    ).all()


def get_order_by_id(
    db: Session,
    order_id: int
):
    return db.query(Order).filter(
        Order.id == order_id
    ).first()

def update_order_status(
        db:Session,
        order:Order,
        status:int
):
    order.status=status

    db.commit()
    db.refresh(order)

    return order

def get_all_orders(
        db:Session
):
    return db.query(Order).all()
