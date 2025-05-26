from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

# Configurações básicas
SECRET_KEY = "your_secret_key"  # 🔐 Substitua por uma ENV segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 5  # ⚠️ Ajuste conforme necessidade

# Criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para gerar hash da senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar se senha corresponde ao hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
