from app.core.database import get_connection

def get_portfolio(user_id: str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT symbol, quantity, avg_price FROM portfolio WHERE user_id=%s",(user_id,))
    portfolio=cursor.fetchall()
    cursor.close()
    conn.close()
    return portfolio