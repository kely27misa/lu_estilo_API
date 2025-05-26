from sqlalchemy import Column, String, Float, Boolean, Integer, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    section = Column(String)
    stock = Column(Integer, default=0)
    expiration_date = Column(Date)
    is_available = Column(Boolean, default=True)

    # ✅ Relacionamento com OrderItem
    order_items = relationship("OrderItem", back_populates="product")
