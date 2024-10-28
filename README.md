# Sistema de Alerta de Preços

Este projeto implementa um sistema de alerta de preços que utiliza a arquitetura **MOM (Message-Oriented Middleware)**, facilitando a comunicação assíncrona entre serviços. A aplicação permite que os usuários definam alertas de preços para produtos. Quando o preço de um produto atinge o limite definido, o sistema envia uma notificação.

Os alertas são gerenciados por meio de uma API criada com **FastAPI**, e a comunicação assíncrona é realizada através do **RabbitMQ**. Os dados de alertas são armazenados no **MongoDB** e os preços dos produtos são atualizados periodicamente.

## Arquitetura MOM (Message-Oriented Middleware)

Este projeto utiliza a arquitetura **MOM**, o que significa que a comunicação entre diferentes serviços é feita de forma assíncrona, via troca de mensagens. No nosso caso, usamos o **RabbitMQ** para enviar e receber mensagens entre os serviços de **alerta** e **notificações**.

A arquitetura MOM é ideal para desacoplar os componentes, garantindo escalabilidade e permitindo que as mensagens sejam processadas de maneira eficiente, mesmo quando alguns serviços estão indisponíveis temporariamente.

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework para criar a API REST.
- **MongoDB**: Banco de dados NoSQL para armazenar alertas e logs de preços.
- **RabbitMQ**: Message broker para comunicação assíncrona entre os serviços.
- **pika**: Cliente Python para interação com RabbitMQ.
- **unittest**: Biblioteca de testes para realizar testes unitários.
- **Docker**: Utilizado para rodar MongoDB e RabbitMQ via Docker Compose.

## Estrutura do Projeto

```bash
/project-root
├── /src
│   ├── /controllers        # Controladores da API, onde as requisições são recebidas e processadas
│   │   └── alerta_controller.py  # Controlador para gerenciar as operações relacionadas aos alertas
│   ├── /services           # Lógica de negócios, comunicação com repositórios e RabbitMQ
│   │   ├── alerta_service.py  # Serviço responsável por criar alertas e enviar mensagens para o RabbitMQ
│   │   ├── notificacao_service.py  # Serviço responsável por receber mensagens do RabbitMQ e enviar notificações (via email)
│   │   └── precos_service.py  # Serviço para atualizar periodicamente os preços dos itens no MongoDB
│   ├── /repositories       # Camada de persistência, responsável por interagir com o banco de dados MongoDB
│   │   └── alerta_repository.py  # Repositório para gerenciar operações CRUD (Create, Read, Update, Delete) de alertas
│   ├── /integrations       # Integração com serviços externos, como RabbitMQ
│   │   └── rabbitmq_client.py  # Cliente para comunicação com o RabbitMQ
│   ├── /models             # Definições dos modelos de dados usando Pydantic
│   │   └── alerta.py  # Modelo de dados de um alerta, utilizado para validação e serialização
│   ├── /config             # Configurações do banco de dados e outras variáveis de ambiente
│   │   └── database.py  # Configuração de conexão com o MongoDB
│   └── /routes             # Definições de rotas da API, usadas para mapear os endpoints
│       └── alerta_routes.py  # Rotas relacionadas aos alertas, como criar, listar, e deletar alertas
├── /tests                  # Testes unitários para as várias partes do sistema
│   ├── /unit               # Testes unitários
│   │   ├── test_alerta_repository.py  # Testes para validar as operações do repositório de alertas
│   │   ├── test_alerta_service.py  # Testes para validar a lógica do serviço de alertas
│   │   └── test_rabbitmq_client.py  # Testes para validar a comunicação com o RabbitMQ
├── .env                    # Arquivo de configuração das variáveis de ambiente (como PYTHONPATH e conexões de banco)
├── requirements.txt        # Lista de dependências do Python que devem ser instaladas
└── docker-compose.yml      # Arquivo para subir os containers do MongoDB e RabbitMQ via Docker Compose
    
```

## Instalação

### Pré-requisitos

- **Python 3.8+**
- **Docker e Docker Compose** (para subir MongoDB e RabbitMQ em contêineres)

1. Clone o repositório e navegue até o diretório do projeto:
   ```bash
   git clone <repo-url>
   cd project-root
   ```

2. Instale as dependências Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no arquivo `.env`.

4. Suba os contêineres do MongoDB e RabbitMQ:
   ```bash
   docker-compose up -d
   ```

## Serviços Principais

### 1. Serviço de Alerta

Para iniciar o serviço que cria alertas e envia mensagens para o **RabbitMQ**, execute o seguinte comando:

```bash
python src/controllers/services/alerta_service.py
```

Este serviço recebe solicitações de criação de alertas e publica mensagens na fila `alertas` do **RabbitMQ**.

### 2. Serviço de Notificações

Para iniciar o serviço que consome as mensagens da fila **RabbitMQ** e envia notificações por email, execute:

```bash
python src/controllers/services/notificacao_service.py
```

Este serviço consome as mensagens de alerta da fila `alertas` e envia notificações (como emails) para os usuários.

### 3. Serviço de Atualização de Preços

Para rodar o serviço que simula a atualização dos preços dos itens no MongoDB de forma periódica, execute o seguinte comando:

```bash
python src/controllers/services/precos_service.py
```

Este serviço atualiza os preços dos itens e armazena o histórico de preços no MongoDB. Ele está configurado para rodar em intervalos de tempo específicos (no exemplo, a cada 10 segundos).

---

## Extensão MongoDB for VS Code

Para facilitar o acesso e gerenciamento do banco de dados MongoDB diretamente do VS Code, você pode instalar a extensão **MongoDB for VS Code**.

### Instalação da Extensão

1. Abra o **VS Code**.
2. Navegue até o painel de **Extensões** (ícone de quadrado à esquerda ou `Ctrl+Shift+X`).
3. Na barra de pesquisa, digite **MongoDB for VS Code** e clique na extensão correspondente (desenvolvida pela MongoDB Inc.).
4. Clique em **Instalar**.

### Configurando a Conexão com MongoDB

Após a instalação:

1. Clique no ícone da extensão **MongoDB** na barra lateral esquerda do VS Code.
2. Clique em **Connect** (ou "Add Connection").
3. Na caixa de diálogo de conexão, insira o endereço do MongoDB, que normalmente é `mongodb://localhost:27017` se você estiver executando o MongoDB localmente via Docker.
4. Clique em **Connect**.

Agora você deve conseguir visualizar e gerenciar as coleções e documentos MongoDB diretamente no VS Code.

---

## Executando os Testes

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

---

Esse `README.md` agora contém todas as instruções para instalar e rodar os serviços principais do sistema, bem como instruções para acessar e gerenciar o MongoDB com a extensão MongoDB for VS Code.
```

