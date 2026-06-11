from fastapi import APIRouter, HTTPException
from app.services.portfolio_service import get_portfolio

router=APIRouter()
@router.get("/portfolio/{user_id}")
def portfolio(user_id:str):
    return get_portfolio(user_id)