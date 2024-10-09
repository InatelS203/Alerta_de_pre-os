# Sistema de Alerta de Preços

Este projeto implementa um sistema de alerta de preços que utiliza a arquitetura **MOM (Message-Oriented Middleware)**, que facilita a comunicação assíncrona entre serviços. A aplicação permite que os usuários definam alertas de preços para produtos. Quando o preço de um produto atinge o limite definido, o sistema envia uma notificação. 

Os alertas são gerenciados por meio de uma API criada com **FastAPI**, e a comunicação assíncrona é realizada através do **RabbitMQ**. Os dados de alertas são armazenados no **MongoDB**.

## Arquitetura MOM (Message-Oriented Middleware)

Este projeto utiliza a arquitetura **MOM**, o que significa que a comunicação entre diferentes serviços é feita de forma assíncrona, via troca de mensagens. No nosso caso, usamos o **RabbitMQ** para enviar e receber mensagens entre os serviços de **alerta** e **notificações**.

A arquitetura MOM é ideal para desacoplar os componentes, garantindo escalabilidade e permitindo que as mensagens sejam processadas de maneira eficiente, mesmo quando alguns serviços estão indisponíveis temporariamente.

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework para criar a API REST.
- **MongoDB**: Banco de dados NoSQL para armazenar alertas e logs de preços.
- **RabbitMQ**: Message broker para comunicação assíncrona entre os serviços.
- **pika**: Cliente Python para interação com RabbitMQ.
- **pytest**: Biblioteca de testes para realizar testes unitários.
- **Docker**: Utilizado para rodar MongoDB e RabbitMQ via Docker Compose.

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
├── /tests                  # Testes unitários
├── .env                    # Variáveis de ambiente
├── requirements.txt         # Dependências do Python
└── docker-compose.yml       # Arquivo para Docker Compose (MongoDB e RabbitMQ)
