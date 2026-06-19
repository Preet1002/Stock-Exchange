from app.core.database import get_connection

def get_balance(user_id: str):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT balance FROM wallets WHERE user_id=%s",(user_id,))
    wallet=cursor.fetchone()
    cursor.close()
    conn.close()
    return wallet

def debit_wallet(cursor,user_id, amount):
    cursor.execute("UPDATE wallets SET balance=balance-%s WHERE user_id=%s",(amount, user_id))

def credit_wallet(cursor,user_id, amount):
    cursor.execute("UPDATE wallets SET balance=balance+%s WHERE user_id=%s",(amount, user_id))

def has_sufficient_balance(user_id, amount):
    wallet=get_balance(user_id)
    return wallet and wallet[0]>=amount

def reserve_funds(cursor, user_id, amount):
    cursor.execute("UPDATE wallets SET balance=balance-%s, reserved=reserved+%s WHERE user_id=%s",(amount, amount, user_id))

def release_funds(cursor, user_id, amount):
    cursor.execute("UPDATE wallets SET balance=balance+%s, reserved=reserved-%s WHERE user_id=%s",(amount, amount, user_id))

def settle_trade(cursor, buyer_id, seller_id, amount):
    cursor.execute("UPDATE wallets SET reserved=reserved-%s WHERE user_id=%s",(amount, buyer_id))
    cursor.execute("UPDATE wallets SET balance=balance+%s WHERE user_id=%s",(amount, seller_id))