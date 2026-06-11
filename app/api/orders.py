from fastapi import APIRouter

from app.schemas.order_schema import OrderRequest
from app.services.order_service import place_order

router=APIRouter(prefix="/orders")

@router.post("/place")
def create_order(order:OrderRequest):
    return place_order(order)