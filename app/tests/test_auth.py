from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4


client = TestClient(app)

def criar_usuario(email: str, password: str, is_admin: bool):
    return client.post("/auth/register", json={
        "email": email,
        "password": password,
        "is_admin": is_admin
    })

def login_usuario(email: str, password: str):
    response = client.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def test_login_com_sucesso():
    criar_usuario("admin_login@teste.com", "123456", is_admin=True)
    response = client.post("/auth/login", json={
        "email": "admin_login@teste.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_criar_pedido_com_user():
    unique = str(uuid4())[:8]
    senha = "123456"
    admin_email = f"admin_{unique}@teste.com"
    user_email = f"user_{unique}@teste.com"

    criar_usuario(admin_email, senha, is_admin=True)
    criar_usuario(user_email, senha, is_admin=False)

    admin_token = login_usuario(admin_email, senha)
    user_token = login_usuario(user_email, senha)

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    cliente_res = client.post("/clients", json={
        "name": "Cliente Teste",
        "email": f"cliente_{unique}@teste.com",
        "cpf": str(uuid4().int)[:11]
    }, headers=admin_headers)
    assert cliente_res.status_code in [200, 201]
    client_id = cliente_res.json()["id"]

    produto_res = client.post("/products", json={
        "name": "Produto Teste",
        "description": "Descrição teste",
        "price": 50.0,
        "barcode": str(uuid4().int)[:12],
        "section": "Testes",
        "stock": 10,
        "expiration_date": "2026-01-01",
        "is_available": True
    }, headers=admin_headers)
    assert produto_res.status_code in [200, 201]
    product_id = produto_res.json()["id"]

    pedido_res = client.post("/orders", json={
        "client_id": client_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ]
    }, headers=user_headers)

    print("Pedido:", pedido_res.status_code, pedido_res.json())

    assert pedido_res.status_code == 201
    data = pedido_res.json()
    assert "id" in data
    assert data["client_id"] == client_id

def test_admin_pode_atualizar_status_pedido():
    unique = str(uuid4())[:8]
    senha = "123456"
    admin_email = f"admin2_{unique}@teste.com"
    user_email = f"user2_{unique}@teste.com"

    criar_usuario(admin_email, senha, is_admin=True)
    criar_usuario(user_email, senha, is_admin=False)

    admin_token = login_usuario(admin_email, senha)
    user_token = login_usuario(user_email, senha)

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {user_token}"}

    cliente_res = client.post("/clients", json={
        "name": "Cliente Atualização",
        "email": f"cliente_update_{unique}@teste.com",
        "cpf": str(uuid4().int)[:11]
    }, headers=admin_headers)
    assert cliente_res.status_code in [200, 201]
    client_id = cliente_res.json()["id"]

    produto_res = client.post("/products", json={
        "name": "Produto Pedido",
        "description": "Teste pedido",
        "price": 20.0,
        "barcode": str(uuid4().int)[:12],
        "section": "Pedidos",
        "stock": 5,
        "expiration_date": "2026-12-31",
        "is_available": True
    }, headers=admin_headers)
    assert produto_res.status_code in [200, 201]
    product_id = produto_res.json()["id"]

    pedido_res = client.post("/orders", json={
        "client_id": client_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
        ]
    }, headers=user_headers)
    assert pedido_res.status_code == 201
    pedido_id = pedido_res.json()["id"]

    # 👇 ADICIONADOS PARA DEBUG
    print("\n--- DEBUG ---")
    print("Pedido criado com ID:", pedido_id)
    print("Tentando PUT /orders/{id} com ID:", pedido_id)
    print("Token do admin:", admin_token[:20] + "...")
    print("----------------")

    update_res = client.put(f"/orders/{pedido_id}", json={
        "status": "shipped"
    }, headers=admin_headers)

    print("Resposta do update:", update_res.status_code, update_res.json())

    assert update_res.status_code == 200
    assert update_res.json()["status"] == "shipped"
