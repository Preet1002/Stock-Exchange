from fastapi import HTTPException
from app.core.database import get_connection
from app.auth.security import verify_password,create_access_token

def login(form_data):
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s",(form_data.username,))
    db_user=cursor.fetchone()
    cursor.close()
    conn.close()
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    token=create_access_token({"sub": db_user["id"]})
    return {
        "access_token": token,
        "token_type": "bearer"
    }