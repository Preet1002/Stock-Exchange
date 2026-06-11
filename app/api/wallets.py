from fastapi import APIRouter, HTTPException
from app.services.wallet_service import get_balance

router=APIRouter()

@router.get("/balance/{user_id}")
def wallet_balance(user_id:str):
    wallet=get_balance(user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
