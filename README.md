# Lu Estilo API

API RESTful desenvolvida com FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Docker e testada com Pytest. Criada como parte do desafio técnico para a InfoG2 (FIAP).

---

## Funcionalidades implementadas

- Autenticação com JWT:
  - Registro de usuários (`/auth/register`)
  - Login com geração de token (`/auth/login`)
  - Proteção de rotas com permissões de admin e usuário
- Clientes:
  - Criar, listar, atualizar e deletar clientes
  - Relacionamento com pedidos
- Produtos:
  - Cadastro com nome, descrição, preço, estoque, seção e validade
- Pedidos:
  - Criação de pedidos por usuários autenticados
  - Verificação de estoque antes de registrar pedido
  - Atualização de status (acesso restrito a admin)
  - Cálculo automático de subtotal e total
- Filtros na listagem de pedidos:
  - Por cliente, status, ID, datas e seção do produto
- Testes automatizados com Pytest
- Banco de dados PostgreSQL com SQLAlchemy
- Containerização com Docker
- Documentação Swagger e Redoc

---

## Como rodar com Docker

docker compose up --build

## Como rodar os testes

docker compose run --rm tests

app/
├── core/ # Segurança e configurações
├── db/ # Sessão e conexão com o banco
├── models/ # Modelos SQLAlchemy
├── routes/ # Rotas organizadas por recurso
├── schemas/ # Schemas Pydantic
├── tests/ # Testes com Pytest
└── main.py # Aplicação FastAPI principal
