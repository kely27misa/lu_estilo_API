from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    cpf = Column(String, unique=True, nullable=False)

    # ✅ Relacionamento com pedidos
    orders = relationship("Order", back_populates="client", cascade="all, delete-orphan")
