from sqlalchemy import Column, String, Boolean
from app.db.session import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # ✅ ESSA LINHA É FUNDAMENTAL
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
