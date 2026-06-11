from app.core.database import get_connection

def get_balance(user_id: str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT balance FROM wallets WHERE user_id=%s",(user_id,))
    wallet=cursor.fetchone()
    cursor.close()
    conn.close()
    return wallet
