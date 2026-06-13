from app.core.database import get_connection
from app.services.wallet_service import debit_wallet, credit_wallet
from app.services.portfolio_service import add_shares, remove_shares
from uuid import uuid4

from app.services.wallet_service import debit_wallet

def find_matching_sell(symbol, buy_price,user_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT * FROM orders where symbol=%s AND side='sell' 
                   AND price<=%s AND status='open' AND user_id!=%s ORDER BY price ASC, 
                   created_at ASC LIMIT 1
                   """, (symbol, buy_price, user_id))
    order=cursor.fetchone()
    cursor.close()
    conn.close()
    return order

def find_matching_buy(symbol, sell_price, user_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT * FROM orders where symbol=%s AND side='buy' 
                   AND price>=%s AND status='open' AND user_id!=%s ORDER BY price DESC, 
                   created_at ASC LIMIT 1
                   """, (symbol, sell_price, user_id))
    order=cursor.fetchone()
    cursor.close()
    conn.close()
    return order

def execute_trade(buy_order, sell_order):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    trade_quantity=min(buy_order['quantity'], sell_order['quantity'])
    trade_price=sell_order['price']
    remaining_buy=buy_order['quantity']-trade_quantity
    remaining_sell=sell_order['quantity']-trade_quantity
    cursor.execute("""
                   INSERT INTO trades (trade_id, buy_order_id, sell_order_id, symbol, price,
                   quantity) VALUES (%s, %s, %s, %s, %s, %s)
                   """, (str(uuid4()), buy_order["order_id"], sell_order["order_id"], 
                         buy_order["symbol"], trade_price, trade_quantity))
    cursor.execute("""UPDATE orders SET quantity=%s, status=%s WHERE order_id=%s""",
                   (remaining_buy, 'filled' if remaining_buy==0 else 'open', buy_order["order_id"]))
    cursor.execute("""UPDATE orders SET quantity=%s, status=%s WHERE order_id=%s""",
                   (remaining_sell, 'filled' if remaining_sell==0 else 'open', sell_order["order_id"]))
    debit_wallet(cursor, buy_order["user_id"], trade_price*trade_quantity)
    credit_wallet(cursor, sell_order["user_id"], trade_price*trade_quantity)  
    add_shares(cursor, buy_order["user_id"], buy_order["symbol"], trade_quantity, trade_price)
    remove_shares(cursor, sell_order["user_id"], sell_order["symbol"], trade_quantity)   
    conn.commit()
    cursor.close()
    conn.close()

def match_order(order_id):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    order=cursor.fetchone()
    cursor.close()
    conn.close()
    if order is None:
        return
    if order['side']=='buy':
        return match_buy_order(order)
    else:
        return match_sell_order(order)
    
def match_buy_order(buy_order):
    while buy_order["quantity"]>0:
        sell_order=find_matching_sell(buy_order["symbol"], buy_order["price"], buy_order["user_id"])
        if sell_order is None:
            break
        execute_trade(buy_order, sell_order)
        buy_order=get_order(buy_order["order_id"])

def match_sell_order(sell_order):
    while sell_order["quantity"]>0:
        buy_order=find_matching_buy(sell_order["symbol"], sell_order["price"], sell_order["user_id"])
        if buy_order is None:
            break
        execute_trade(buy_order, sell_order)
        sell_order=get_order(sell_order["order_id"])
    
def get_order(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM orders WHERE order_id=%s",
        (order_id,)
    )

    order = cursor.fetchone()

    cursor.close()
    conn.close()

    return order