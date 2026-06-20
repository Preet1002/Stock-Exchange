from uuid import uuid4
from fastapi import HTTPException
from app.core.database import get_connection
from app.services.matching_engine import match_order
from app.services.wallet_service import has_sufficient_balance
from app.services.portfolio_service import has_sufficient_shares
from app.services.wallet_service import release_funds, reserve_funds

def place_order(order,current_user):
    conn=get_connection()
    cursor=conn.cursor()
    trade_value=order.price*order.quantity
    if order.side=="buy":
        if not has_sufficient_balance(current_user, trade_value):
            raise HTTPException(status_code=400, detail="Insufficient balance")
        reserve_funds(cursor, current_user, trade_value)
    if order.side=="sell":
        if not has_sufficient_shares(current_user, order.symbol, order.quantity):
            raise HTTPException(status_code=400, detail="Insufficient shares")
    order_id=str(uuid4())
    cursor.execute("""INSERT INTO orders (
                   order_id, user_id, symbol,side, price,quantity) 
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                    (order_id, current_user, order.symbol,
                      order.side, order.price, order.quantity))
    conn.commit()
    cursor.close()
    conn.close()
    match_order(order_id)
    return {
        "order_id": order_id,
        "status": "submitted"
    }

def cancel_order(order_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    order=cursor.fetchone()
    if order is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    if order["status"]!="open":
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    if order["side"]=="buy":
        release_funds(cursor, order["user_id"], order["price"]*order["quantity"])
    cursor.execute("UPDATE orders SET status='cancelled' WHERE order_id=%s", (order_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "status": "cancelled"
    }

def get_order_history(user_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE user_id=%s ORDER BY created_at DESC", (user_id,))
    orders=cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

def get_trade_history(user_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT t.trade_id,t.symbol,t.price,t.quantity,t.created_at,
                   CASE WHEN o.user_id=%s THEN 'buy' ELSE 'sell' END AS side
                   FROM trades t JOIN orders o ON t.buy_order_id=o.order_id
                   WHERE o.user_id=%s UNION
                   SELECT t.trade_id,t.symbol,t.price,t.quantity,t.created_at, 'sell'
                   FROM trades t JOIN orders o ON t.sell_order_id=o.order_id
                   WHERE o.user_id=%s ORDER BY created_at DESC
                   """, (user_id, user_id,user_id))
    trades=cursor.fetchall()
    cursor.close()
    conn.close()
    return trades