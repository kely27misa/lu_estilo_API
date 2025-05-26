# Lu Estilo API

API RESTful desenvolvida com FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Docker e testada com Pytest. Criada como parte do desafio técnico para a InfoG2.

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
A API ficará disponível em: http://localhost:8000

Documentação Swagger: http://localhost:8000/docs

Como rodar os testes

docker compose run --rm tests
Os testes cobrem:

Autenticação e proteção de rotas

Criação de pedidos e verificação de estoque

Atualização de status de pedido

Filtros por status, cliente, data e seção

Estrutura do projeto

app/
├── core/ # Segurança e configurações
├── db/ # Sessão e conexão com o banco
├── models/ # Modelos SQLAlchemy
├── routes/ # Rotas organizadas por recurso
├── schemas/ # Schemas Pydantic
├── tests/ # Testes com Pytest
└── main.py # Aplicação FastAPI principal

A fazer
Paginação na listagem de pedidos

Filtros adicionais na listagem de produtos

Upload de imagens para produtos

Deploy em nuvem (ex: Render, Railway)

Integração contínua com GitHub Actions

Logging estruturado

Proteção contra brute-force ou rate limiting

Desenvolvedora Kely dos santos
Este projeto foi desenvolvido como parte do processo seletivo para a InfoG2, com foco em arquitetura limpa, autenticação segura e testes automatizados.

```

```
