from pydantic import BaseModel,ConfigDict
from enum import Enum

class OrderStatus(str,Enum):
    pending="pending"
    confirmed="confirmed"
    shipped="shipped"
    delivered="delivered"
    cancelled="cancelled"

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str

    model_config=ConfigDict(from_attributes=True)
