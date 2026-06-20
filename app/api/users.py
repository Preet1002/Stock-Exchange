from fastapi import APIRouter, HTTPException
from uuid import uuid4
from app.core.database import get_connection
from app.schemas.user_schema import CreateUserRequest
from app.auth.security import hash_password

router =APIRouter()
@router.post("/users")
def create_user(user: CreateUserRequest):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (user.username,)
    )
    if cursor.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    user_id=str(uuid4())
    hashed_password=hash_password(user.password)
    cursor.execute(
        """INSERT INTO users(id,username,password)
        VALUES(%s,%s,%s)""",
        (user_id,user.username,hashed_password)
    )
    cursor.execute(
        """INSERT INTO wallets(user_id,balance,reserved)
        VALUES(%s,%s,%s)""",
        (user_id,10000.00,0.00)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "id": user_id,
        "username": user.username,
        "wallet_balance": 10000.00
    }