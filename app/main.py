from fastapi import FastAPI
from app.routes import auth, clients, products, orders
from app.db.session import Base, engine

# Importa os modelos para criação automática de tabelas
from app.models import product, client, order, order_item

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Inicializa o app
app = FastAPI(title="Lu Estilo API")

# Registra as rotas
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)  # ✅ Agora sim, corretamente incluída

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()
