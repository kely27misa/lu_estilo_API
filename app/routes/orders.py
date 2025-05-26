from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.client import Client
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.core.dependencies import get_current_user, get_admin_user

router = APIRouter(prefix="/orders", tags=["Orders"])

# ✅ Criar pedido (usuário autenticado)
@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == order_data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    order = Order(
        id=str(uuid4()),
        client_id=order_data.client_id,
        status=OrderStatus.PENDING,
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.flush()
    db.refresh(order)

    total_order = 0.0

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")

        product.stock -= item.quantity
        subtotal = product.price * item.quantity
        total_order += subtotal

        order_item = OrderItem(
            id=str(uuid4()),
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
            subtotal=subtotal
        )
        db.add(order_item)

    order.total = total_order
    db.commit()
    db.refresh(order)
    return order

# ✅ Atualizar status (admin)
@router.put("/{id}", response_model=OrderResponse)
def update_order_status(
    id: str,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = update_data.status
    db.commit()
    db.refresh(order)
    return order

# ✅ Listar pedidos com filtros (usuário autenticado)
@router.get("/", response_model=List[OrderResponse])
def list_orders(
    client_id: Optional[str] = None,
    status: Optional[OrderStatus] = None,
    order_id: Optional[str] = None,
    section: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Order)

    if client_id:
        query = query.filter(Order.client_id == client_id)
    if status:
        query = query.filter(Order.status == status)
    if order_id:
        query = query.filter(Order.id == order_id)
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)
    if section:
        query = query.join(Order.items).join(OrderItem.product).filter(Product.section == section)

    return query.all()
