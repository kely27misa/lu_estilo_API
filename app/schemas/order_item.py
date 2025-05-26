from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int

class OrderItemResponse(OrderItemCreate):
    id: str
    subtotal: float

    class Config:
        from_attributes = True
