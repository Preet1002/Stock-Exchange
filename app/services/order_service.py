from uuid import uuid4
from fastapi import HTTPException
from app.core.database import get_connection
from app.services.matching_engine import match_order
from app.services.wallet_service import has_sufficient_balance
from app.services.portfolio_service import has_sufficient_shares

def place_order(order):
    trade_value=order.price*order.quantity
    if order.side=="buy":
        if not has_sufficient_balance(order.user_id, trade_value):
            raise HTTPException(status_code=400, detail="Insufficient balance")
    if order.side=="sell":
        if not has_sufficient_shares(order.user_id, order.symbol, order.quantity):
            raise HTTPException(status_code=400, detail="Insufficient shares")
    conn=get_connection()
    cursor=conn.cursor()
    order_id=str(uuid4())
    cursor.execute("""INSERT INTO orders (
                   order_id, user_id, symbol,side, price,quantity) 
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                    (order_id, order.user_id, order.symbol,
                      order.side, order.price, order.quantity))
    conn.commit()
    cursor.close()
    conn.close()
    match_order(order_id)
    return {
        "order_id": order_id,
        "status": "submitted"
    }