from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schemas.order import OrderResponse  # ✅ Importa para relacionar os pedidos do cliente

# ✅ Schema para criação de cliente (POST /clients)
class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str

# ✅ Schema para atualização parcial de cliente (PUT /clients/{id})
class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None

# ✅ Schema de resposta, incluindo os pedidos associados
class ClientResponse(ClientCreate):
    id: str
    orders: Optional[List[OrderResponse]] = []  # Lista de pedidos

    class Config:
        from_attributes = True
