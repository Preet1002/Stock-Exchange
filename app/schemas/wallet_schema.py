from pydantic import BaseModel
class DepositRequest(BaseModel):
    amount: float
class WithdrawRequest(BaseModel):
    amount: float