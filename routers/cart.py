from fastapi import APIRouter, Depends, HTTPException,Query

from database import get_db
from utils.auth import get_current_user

from services.cart_service import (
    add_to_cart,
    get_my_cart,
    remove_from_cart,
    update_cart_quantity
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/add")
def add_product_to_cart(
    product_id: int,
    quantity: int=Query(1,gt=0),
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):

    cart_item=add_to_cart(
        db,
        current_user.id,
        product_id,
        quantity
    )

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )

    return cart_item

@router.get("/")
def view_my_cart(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_my_cart(
        db,
        current_user.id
    )


@router.delete("/remove/{product_id}")
def remove_product_from_cart(
    product_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = remove_from_cart(
        db,
        current_user.id,
        product_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )

    return {
        "message": "Product removed from cart"
    }


@router.put("/update/{product_id}")
def update_product_quantity(
    product_id: int,
    quantity: int=Query(...,gt=0),
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    cart_item = update_cart_quantity(
        db,
        current_user.id,
        product_id,
        quantity
    )

    if cart_item is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )

    return cart_item