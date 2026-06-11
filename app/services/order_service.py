from uuid import uuid4
from app.core.database import get_connection

def place_order(order):
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
    return {
        "order_id": order_id,
        "status": "open"
    }