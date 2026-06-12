from app.core.database import get_connection

def get_orderbook(symbol):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT price, quantity FROM orders WHERE symbol=%s
                    AND side='buy' AND status='open' ORDER BY price DESC, created_at ASC
                   """, (symbol,))
    bids=cursor.fetchall()
    cursor.execute("""
                     SELECT price, quantity FROM orders WHERE symbol=%s
                   AND side='sell' AND status='open' ORDER BY price ASC, created_at ASC
                     """, (symbol,))
    asks=cursor.fetchall()
    cursor.close()
    conn.close()
    return {
        "symbol": symbol,
        "bids": bids,
        "asks": asks
    }