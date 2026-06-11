from pydantic import BaseModel
class PortfolioItem(BaseModel):
    stock_symbol: str
    quantity: int
    avg_price: float