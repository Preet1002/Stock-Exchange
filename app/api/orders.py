from fastapi import APIRouter

from app.schemas.order_schema import OrderRequest
from app.services.order_service import place_order
from app.services.order_service import cancel_order

router=APIRouter(prefix="/orders")

@router.post("/place")
def create_order(order:OrderRequest):
    return place_order(order)

@router.delete("/cancel/{order_id}")
def cancel(order_id:str):
    return cancel_order(order_id)