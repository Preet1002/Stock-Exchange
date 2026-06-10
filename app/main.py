from fastapi import FastAPI
from app.api.users import router as user_router
app=FastAPI(
    title="Stock Exchange"
)
app.include_router(user_router)
@app.get("/")
def root():
    return {
        "message": "Stock Exchange running"
        }