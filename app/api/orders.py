from fastapi import APIRouter

from app.schemas.order_schema import OrderRequest
from app.services.order_service import place_order
from app.services.order_service import cancel_order,get_order_history, get_trade_history

router=APIRouter(prefix="/orders")

@router.post("/place")
def create_order(order:OrderRequest):
    return place_order(order)

@router.delete("/cancel/{order_id}")
def cancel(order_id:str):
    return cancel_order(order_id)

@router.get("/history/{user_id}")
def order_history(user_id: str):
    return get_order_history(user_id)

@router.get("/trades/{user_id}")
def trade_history(user_id: str):
    return get_trade_history(user_id)