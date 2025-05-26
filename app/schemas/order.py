from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from enum import Enum


# ✅ Enum para status dos pedidos
class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    canceled = "canceled"


# ✅ Schema para criação de pedido
class OrderCreate(BaseModel):
    client_id: str
    items: List[OrderItemCreate]


# ✅ Schema para resposta de pedido
class OrderResponse(BaseModel):
    id: str
    client_id: str
    created_at: datetime
    total: float
    status: OrderStatus
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


# ✅ Schema para atualização de status do pedido
class OrderUpdate(BaseModel):
    status: OrderStatus
