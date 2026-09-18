from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from utils.auth import get_current_user, require_admin

from schemas.order import OrderResponse,OrderStatus

from services.order_service import (
    place_order,
    get_my_orders,
    get_order,
    change_order_status,
    get_all_orders_for_admin
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def create_new_order(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = place_order(
        db,
        current_user.id
    )

    if order is None:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    return order


@router.get("/")
def view_my_orders(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_my_orders(
        db,
        current_user.id
    )


@router.get("/admin/all")
def view_all_orders(
    db=Depends(get_db),
    current_user=Depends(require_admin)
):
    return get_all_orders_for_admin(db)


@router.get("/{order_id}")
def view_order(
    order_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = get_order(
        db,
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this order"
        )

    return order


@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status:OrderStatus,
    db=Depends(get_db),
    current_user=Depends(require_admin)
):
    order = change_order_status(
        db,
        order_id,
        status
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order
