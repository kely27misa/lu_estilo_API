from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4

from app.db.session import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.core.dependencies import get_current_user, get_admin_user
from sqlalchemy.orm import joinedload


router = APIRouter(prefix="/clients", tags=["Clients"])

# ✅ Qualquer usuário autenticado pode listar
@router.get("/", response_model=List[ClientResponse])
def list_clients(
    name: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()

# ✅ Somente admin pode criar cliente
@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    # Verifica se email ou CPF já existem
    existing_email = db.query(Client).filter(Client.email == client_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_cpf = db.query(Client).filter(Client.cpf == client_data.cpf).first()
    if existing_cpf:
        raise HTTPException(status_code=400, detail="CPF already registered")

    client = Client(id=str(uuid4()), **client_data.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

# ✅ Qualquer usuário autenticado pode buscar por ID
@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(
    client_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    client = db.query(Client).options(joinedload(Client.orders)).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# ✅ Somente admin pode atualizar cliente
@router.put("/{id}", response_model=ClientResponse)
def update_client(
    id: str,
    updates: ClientUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client

# ✅ Somente admin pode deletar cliente
@router.delete("/{id}", status_code=204)
def delete_client(
    id: str,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
