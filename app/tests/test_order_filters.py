from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

def test_listar_pedidos_filtrando_por_status():
    # Cria usuário admin
    admin_email = f"admin_{uuid4()}@teste.com"
    client.post("/auth/register", json={
        "email": admin_email,
        "password": "123456",
        "is_admin": True
    })
    login_res = client.post("/auth/login", json={
        "email": admin_email,
        "password": "123456"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria cliente
    cliente_res = client.post("/clients", json={
        "name": "Cliente Filtro",
        "email": f"cliente_filtro_{uuid4()}@teste.com",
        "cpf": str(uuid4().int)[:11]
    }, headers=headers)
    client_id = cliente_res.json()["id"]

    # Cria produto
    produto_res = client.post("/products", json={
        "name": "Produto Filtro",
        "description": "Produto para teste de filtro",
        "price": 10.0,
        "barcode": str(uuid4().int)[:12],
        "section": "Filtros",
        "stock": 5,
        "expiration_date": "2026-12-31",
        "is_available": True
    }, headers=headers)
    product_id = produto_res.json()["id"]

    # Cria pedido
    pedido_res = client.post("/orders", json={
        "client_id": client_id,
        "items": [
            {"product_id": product_id, "quantity": 1}
        ]
    }, headers=headers)
    assert pedido_res.status_code == 201

    # Testa filtro por status
    filtro_res = client.get("/orders", params={"status": "pending"}, headers=headers)
    assert filtro_res.status_code == 200
    assert any(order["status"] == "pending" for order in filtro_res.json())

def test_erro_se_estoque_insuficiente():
    from time import time
    unique = str(int(time()))
    email = f"admin_{unique}@teste.com"

    # Cria admin
    client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "is_admin": True
    })
    login = client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria cliente
    cliente = client.post("/clients", json={
        "name": "Cliente Estoque",
        "email": f"cliente_estoque_{unique}@teste.com",
        "cpf": str(uuid4().int)[:11]
    }, headers=headers)
    client_id = cliente.json()["id"]

    # Cria produto com estoque 1
    produto = client.post("/products", json={
        "name": "Produto Limitado",
        "description": "Tem pouco estoque",
        "price": 99.0,
        "barcode": str(uuid4().int)[:12],
        "section": "Estoque",
        "stock": 1,
        "expiration_date": "2026-12-31",
        "is_available": True
    }, headers=headers)
    product_id = produto.json()["id"]

    # Tenta criar pedido com quantity = 5 (acima do estoque)
    pedido = client.post("/orders", json={
        "client_id": client_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 5
            }
        ]
    }, headers=headers)

    assert pedido.status_code == 400
    assert "stock" in pedido.json()["detail"].lower()

def test_filtro_por_secao():
    from time import time
    unique = str(int(time()))
    email = f"admin_{unique}@teste.com"

    # Cria admin
    client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "is_admin": True
    })
    login = client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Cria cliente
    cliente = client.post("/clients", json={
        "name": "Cliente Filtro",
        "email": f"cliente_filtro_{unique}@teste.com",
        "cpf": str(uuid4().int)[:11]
    }, headers=headers)
    client_id = cliente.json()["id"]

    # Cria dois produtos em seções diferentes
    prod1 = client.post("/products", json={
        "name": "Batom Rosa",
        "description": "Produto de beleza",
        "price": 10.0,
        "barcode": str(uuid4().int)[:12],
        "section": "Beleza",
        "stock": 10,
        "expiration_date": "2026-12-31",
        "is_available": True
    }, headers=headers)
    prod2 = client.post("/products", json={
        "name": "Martelo",
        "description": "Ferramenta",
        "price": 25.0,
        "barcode": str(uuid4().int)[:12],
        "section": "Ferramentas",
        "stock": 10,
        "expiration_date": "2026-12-31",
        "is_available": True
    }, headers=headers)

    prod1_id = prod1.json()["id"]
    prod2_id = prod2.json()["id"]

    # Cria dois pedidos com produtos em seções diferentes
    client.post("/orders", json={
        "client_id": client_id,
        "items": [
            {"product_id": prod1_id, "quantity": 1}
        ]
    }, headers=headers)

    client.post("/orders", json={
        "client_id": client_id,
        "items": [
            {"product_id": prod2_id, "quantity": 1}
        ]
    }, headers=headers)

    # Busca pedidos com filtro section="Beleza"
    filtro = client.get("/orders?section=Beleza", headers=headers)
    assert filtro.status_code == 200
    results = filtro.json()
    assert all(
        any(item["product_id"] == prod1_id for item in pedido["items"])
        for pedido in results
    )
