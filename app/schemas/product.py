from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    barcode: str
    section: str
    stock: int
    expiration_date: str
    is_available: bool


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    expiration_date: Optional[str] = None
    is_available: Optional[bool] = None


class ProductResponse(ProductCreate):
    id: str

    class Config:
        from_attributes = True
