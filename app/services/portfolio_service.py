from app.core.database import get_connection

def get_portfolio(user_id: str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT symbol, quantity, avg_price FROM portfolio WHERE user_id=%s",(user_id,))
    portfolio=cursor.fetchall()
    cursor.close()
    conn.close()
    return portfolio

def add_shares(cursor, user_id, symbol, quantity, trade_price):
    cursor.execute("SELECT quantity, avg_price FROM portfolio WHERE user_id=%s AND symbol=%s",(user_id, symbol))
    stock=cursor.fetchone()
    if stock:
        new_quantity=stock["quantity"]+quantity
        new_avg_price=((stock["quantity"]*stock["avg_price"])+(quantity*trade_price))/new_quantity
        cursor.execute("UPDATE portfolio SET quantity=%s, avg_price=%s WHERE user_id=%s AND symbol=%s",
                       (new_quantity, new_avg_price, user_id, symbol))
    else:
        cursor.execute("INSERT INTO portfolio (user_id, symbol, quantity, avg_price) VALUES (%s, %s, %s, %s)",
                       (user_id, symbol, quantity, trade_price))
        
def remove_shares(cursor, user_id, symbol, quantity):
    cursor.execute("SELECT quantity FROM portfolio WHERE user_id=%s AND symbol=%s",(user_id, symbol))
    stock=cursor.fetchone()
    if stock is None:
        return
    remaining=stock["quantity"]-quantity
    if remaining==0:
        cursor.execute("DELETE FROM portfolio WHERE user_id=%s AND symbol=%s",(user_id, symbol))
    else:
        cursor.execute("UPDATE portfolio SET quantity=%s WHERE user_id=%s AND symbol=%s",
                           (remaining, user_id, symbol))