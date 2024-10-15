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
│   ├── /controllers        # Controladores da API, onde as requisições são recebidas e processadas
│   │   └── alerta_controller.py
│   ├── /services           # Lógica de negócios, comunicação com repositórios e RabbitMQ
│   │   ├── alerta_service.py
│   │   └── notificacao_service.py
│   ├── /repositories       # Camada de persistência, interação com o banco de dados MongoDB
│   │   └── alerta_repository.py
│   ├── /integrations       # Integração com serviços externos, como RabbitMQ
│   │   └── rabbitmq_client.py
│   ├── /models             # Definições dos modelos de dados usando Pydantic
│   │   └── alerta.py
│   ├── /config             # Configurações do banco de dados e outras variáveis
│   │   └── database.py
│   └── /routes             # Definições de rotas da API
│       └── alerta_routes.py
├── /tests                  # Testes unitários para as várias partes do sistema
│   ├── /unit               # Testes unitários
│   │   ├── test_alerta_repository.py
│   │   ├── test_alerta_service.py
│   │   └── test_rabbitmq_client.py
├── .env                    # Arquivo de configuração das variáveis de ambiente (como PYTHONPATH)
├── requirements.txt        # Lista de dependências do Python que devem ser instaladas
└── docker-compose.yml      # Arquivo para subir os containers do MongoDB e RabbitMQ via Docker Compose

## Configuração e Execução

1. Pré-requisitos
Antes de iniciar o projeto, certifique-se de que você tenha instalado:

-Python 3.x
-Docker e Docker Compose

2. Instalar Dependências
Após clonar o repositório, instale as dependências do projeto com o comando:

-**pip install -r requirements.txt**

## 3. Configurar o PYTHONPATH
Para que o Python reconheça os módulos corretamente, é importante configurar o PYTHONPATH. Isso pode ser feito através do .env ou diretamente no VS Code.

Usando o Arquivo .env
-**Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

PYTHONPATH=./src

Aqui está a seção completa formatada em Markdown:

```markdown
## Configuração e Execução

### 1. Pré-requisitos

Antes de iniciar o projeto, certifique-se de que você tenha instalado:

- **Python 3.x**
- **Docker** e **Docker Compose**

### 2. Instalar Dependências

Após clonar o repositório, instale as dependências do projeto com o comando:

```bash
pip install -r requirements.txt
```

### 3. Configurar o PYTHONPATH

Para que o Python reconheça os módulos corretamente, é importante configurar o **PYTHONPATH**. Isso pode ser feito através do **`.env`** ou diretamente no **VS Code**.

#### Usando o Arquivo `.env`

Crie um arquivo **`.env`** na raiz do projeto com o seguinte conteúdo:

```bash
PYTHONPATH=./src
```

#### Configurando o PYTHONPATH no VS Code

Se estiver usando o **VS Code**, você também pode adicionar o seguinte ao arquivo **`settings.json`**:

```json
{
    "python.analysis.extraPaths": [
        "./src"
    ],
    "python.envFile": "${workspaceFolder}/.env",
    "python.testing.unittestArgs": [
        "-v",  // Detalhamento dos testes
        "-s", "./tests",  // Diretório de testes
        "-p", "*_test.py"  // Padrão de nome dos arquivos de teste
    ],
    "python.testing.pytestEnabled": false,  // Desabilita pytest (usando unittest)
    "python.testing.unittestEnabled": true  // Habilita unittest
}
```

### 4. Subir MongoDB e RabbitMQ com Docker

Para rodar o MongoDB e RabbitMQ usando Docker Compose, execute o seguinte comando na raiz do projeto:

```bash
docker-compose up -d
```

Isso irá subir os containers com o MongoDB e RabbitMQ.

### 5. Rodar a API FastAPI

Agora você pode iniciar a API FastAPI com o seguinte comando:

```bash
python src/routes/alerta_routes.py
```

A API estará disponível em `http://localhost:8000`.

---

## Executando os Testes

### 1. Rodar os Testes no VS Code

Se estiver utilizando o **VS Code**, você pode rodar os testes diretamente no painel de testes:

1. Vá até o ícone de "Testes" na barra lateral.
2. Clique em **Run All Tests** para executar todos os testes.

### 2. Rodar os Testes no Terminal

Para rodar os testes manualmente pelo terminal, use o seguinte comando:

#### No Windows:

```bash
set PYTHONPATH=src && python -m unittest discover -s tests -p "*_test.py"
```

#### No Linux/macOS:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p "*_test.py"
```

Esse comando rodará todos os testes localizados no diretório `tests`.

---

## Endpoints da API

### 1. Criar Alerta

```http
POST /alertas
```

**Request Body (JSON):**

```json
{
  "usuario_id": "123",
  "produto": "Smartphone XYZ",
  "preco_limite": 1000.0,
  "data_criacao": "2024-09-02",
  "status": "ativo"
}
```

**Response:**

```json
{
  "message": "Alerta criado com sucesso!"
}
```

### 2. Listar Alertas

```http
GET /alertas
```

**Response:**

```json
[
  {
    "usuario_id": "123",
    "produto": "Smartphone XYZ",
    "preco_limite": 1000.0,
    "data_criacao": "2024-09-02",
    "status": "ativo"
  }
]
```

---

## Contribuindo

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nome-da-feature`).
5. Abra um Pull Request.
```

