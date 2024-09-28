# Sistema de Alerta de Preços

Este projeto é um sistema de alerta de preços que utiliza uma arquitetura **MOM (Message-Oriented Middleware)**. Ele permite que os usuários definam alertas de preços para produtos e, quando o preço de um produto atinge o limite definido, o sistema envia uma notificação. O backend é construído com **FastAPI**, e a comunicação assíncrona é gerenciada com **RabbitMQ**. Os dados de alertas são armazenados em **MongoDB**.

## Tecnologias Utilizadas
- **Python** (v3.x)
- **FastAPI**: Framework para criação da API REST.
- **MongoDB**: Banco de dados NoSQL para armazenar alertas e logs de preços.
- **RabbitMQ**: Message broker para gerenciar a comunicação assíncrona.
- **pika**: Cliente Python para RabbitMQ.
- **Docker**: Usado para rodar MongoDB e RabbitMQ via Docker Compose.

## Estrutura do Projeto
```bash
/project-root
├── /src
│   ├── /controllers        # Controladores de rotas da API
│   ├── /services           # Lógica de negócios e comunicação com RabbitMQ
│   ├── /repositories       # Camada de persistência (MongoDB)
│   ├── /integrations       # Integração com RabbitMQ e APIs externas
│   ├── /models             # Definições dos modelos de dados (Pydantic)
│   ├── /config             # Configuração de banco de dados (MongoDB)
│   └── /routes             # Definição das rotas da API
├── /tests                  # Testes unitários e de integração
├── .env                    # Arquivo de configuração do ambiente
├── docker-compose.yml       # Docker Compose para MongoDB e RabbitMQ
├── requirements.txt         # Dependências do Python
└── README.md                # Este arquivo
