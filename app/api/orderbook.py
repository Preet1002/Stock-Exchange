from fastapi import APIRouter
from app.services.orderbook_service import get_orderbook

router=APIRouter(prefix="/orderbook")

@router.get("/{symbol}")
def orderbook(symbol:str):
    return get_orderbook(symbol)