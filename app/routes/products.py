from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
from sqlalchemy import and_

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.core.dependencies import get_current_user, get_admin_user  # IMPORTANTE

router = APIRouter(prefix="/products", tags=["Products"])

# ✅ Somente admin pode criar produto
@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)  # ← aqui validamos se é admin
):
    if db.query(Product).filter(Product.barcode == product_data.barcode).first():
        raise HTTPException(status_code=400, detail="Barcode already registered")

    product = Product(id=str(uuid4()), **product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# ✅ Qualquer usuário autenticado pode listar produtos com filtros
@router.get("/", response_model=List[ProductResponse])
def list_products(
    section: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Product)

    if section:
        query = query.filter(Product.section.ilike(f"%{section}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)

    return query.offset(skip).limit(limit).all()

# ✅ Qualquer usuário autenticado pode ver um produto específico
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ✅ Somente admin pode atualizar produto
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    updates: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)  # ← só admin aqui
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

# ✅ Somente admin pode deletar produto
@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)  # ← só admin aqui também
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
