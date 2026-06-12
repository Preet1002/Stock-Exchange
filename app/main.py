from fastapi import FastAPI
from app.api.users import router as user_router
from app.api.wallets import router as wallet_router
from app.api.portfolio import router as portfolio_router
from app.api.orders import router as order_router
from app.api.orderbook import router as orderbook_router
app=FastAPI(
    title="Stock Exchange"
)
app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(orderbook_router)
app.include_router(order_router)
app.include_router(portfolio_router)
@app.get("/")
def root():
    return {
        "message": "Stock Exchange running"
        }