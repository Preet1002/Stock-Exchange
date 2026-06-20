from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import login

router=APIRouter()

@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm=Depends()):
    return login(form_data)
