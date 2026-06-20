from pydantic import BaseModel
from enum import Enum

class OrderSide(str, Enum):
    BUY="buy"
    SELL="sell"
class OrderRequest(BaseModel):
    symbol: str
    side: OrderSide
    price: float
    quantity: int