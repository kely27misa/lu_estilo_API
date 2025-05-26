# lu-estilo-api

🧵 **Lu Estilo API** — Uma API RESTful para gerenciamento de clientes, produtos e pedidos de uma loja de roupas, construída com **FastAPI + PostgreSQL + Docker**.

## ✅ Tecnologias usadas

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Docker + Docker Compose
- Pytest
- JWT Authentication

## 📦 Estrutura atual do projeto

- **Autenticação de usuários (admin e comum)**
- **CRUD de Clientes**
- **CRUD de Produtos**
- **Criação de Pedidos**
- **Atualização de status do pedido (admin)**
- **Listagem de pedidos com filtros:**
  - `status`
  - `client_id`
  - `order_id`
  - `section`
  - `start_date`, `end_date`
- **Testes automatizados com Pytest**

## 🔍 Testes implementados

- Login válido
- Criação de pedido por usuário comum
- Atualização de pedido por admin
- Listagem de pedidos com filtros

## 🧪 Como rodar os testes

```bash
docker compose run --rm -e PYTHONPATH=/code tests
```
