# Sistema de Alerta de Preços

Este projeto implementa um sistema de alerta de preços que utiliza a arquitetura **MOM (Message-Oriented Middleware)**, facilitando a comunicação assíncrona entre serviços. A aplicação permite que os usuários definam alertas de preços para produtos. Quando o preço de um produto atinge o limite definido, o sistema envia uma notificação via SMS usando a API do Twilio.

Os alertas são gerenciados por meio de uma API criada com **FastAPI**, e a comunicação assíncrona é realizada através do **RabbitMQ**. Os dados de alertas são armazenados no **MongoDB** e os preços dos produtos são atualizados periodicamente.

---

## Arquitetura MOM (Message-Oriented Middleware)

Este projeto utiliza a arquitetura **MOM**, o que significa que a comunicação entre diferentes serviços é feita de forma assíncrona, via troca de mensagens. Neste caso, o **RabbitMQ** é utilizado para enviar e receber mensagens entre os serviços de **alerta** e **notificações**.

A arquitetura MOM é ideal para desacoplar os componentes, garantindo escalabilidade e permitindo que as mensagens sejam processadas de maneira eficiente, mesmo quando alguns serviços estão indisponíveis temporariamente.

---

## Design Patterns Utilizados

### 1. **Strategy Pattern**
Usado para encapsular diferentes formas de envio de notificações. Atualmente, a implementação utiliza o envio de **SMS** como estratégia padrão. 
- **Classe Base**: `NotificationStrategy`
- **Implementação Específica**: `SMSNotification`
- **Motivo**: Permitir a inclusão futura de novos métodos de notificação (ex.: e-mail, WhatsApp) sem alterar a lógica principal.

### 2. **Singleton Pattern**
Aplicado à conexão com o banco de dados **MongoDB**, garantindo que apenas uma instância do cliente seja criada e reutilizada em todo o sistema.
- **Classe**: `MongoClient` (implementação nativa no MongoDB).
- **Motivo**: Evita múltiplas conexões ao banco, otimizando o desempenho e reduzindo custos.

### 3. **Repository Pattern**
Utilizado para encapsular a lógica de acesso ao banco de dados. Isso separa a lógica de persistência da lógica de negócios.
- **Classe**: `AlertaRepository`
- **Motivo**: Facilita a manutenção e a troca do banco de dados, caso necessário.

---

### 1. **Strategy**
- Permite alternar entre diferentes formas de notificação (ex.: SMS, e-mail) sem modificar o código principal.
- **Classe Base**: `NotificationStrategy`
  - Implementação: `SMSNotification`
  - Localização: `src/controllers/strategies/notification_strategy.py`
- **Uso**: 
  - No `NotificacaoService`, a estratégia é usada para enviar notificações:
    ```python
    self.notification_strategy.send_notification(alerta)
    ```

### 2. **Singleton**
- Garante uma única instância para a conexão com o MongoDB.
- **Localização**: `src/config/database.py`
  - Função: `get_database()`
  - Implementa e reutiliza a conexão:
    ```python
    client = MongoClient("mongodb://localhost:27017/")
    return client["sistema_precos"]
    ```

### 3. **Repository**
- Encapsula a lógica de acesso ao banco de dados.
- **Classe**: `AlertaRepository`
  - Métodos: `buscar_alertas_ativos`, `salvar_alerta`
  - Localização: `src/controllers/repositories/alerta_repository.py`
- **Uso**: 
  - No `NotificacaoService`:
    ```python
    alertas = self.repository.buscar_alertas_ativos()
    ```

---

---

## Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI**: Framework para criar a API REST.
- **MongoDB**: Banco de dados NoSQL para armazenar alertas e logs de preços.
- **RabbitMQ**: Message broker para comunicação assíncrona entre os serviços.
- **Twilio API**: Serviço para envio de notificações via SMS.
- **pika**: Cliente Python para interação com RabbitMQ.
- **unittest**: Biblioteca de testes para realizar testes unitários.

---

```bash
/project-root
├── /src
│   ├── /controllers           # Controladores da API
│   │   └── alerta_controller.py # Controlador para gerenciar alertas
│   ├── /services              # Serviços de negócios e comunicação
│   │   ├── alerta_service.py     # Serviço para criação de alertas
│   │   ├── notificacao_service.py # Serviço para envio de notificações via SMS
│   │   └── precos_service.py     # Serviço para monitorar e atualizar preços
│   ├── /repositories          # Camada de persistência
│   │   └── alerta_repository.py  # Repositório para CRUD de alertas
│   ├── /strategies            # Estratégias de notificação
│   │   ├── notification_strategy.py # Interface e implementação do Strategy Pattern
│   │   └── notification_factory.py  # Fábrica para criação de estratégias
│   ├── /integrations          # Integrações externas
│   │   └── rabbitmq_client.py    # Cliente para RabbitMQ
│   ├── /models                # Modelos de dados
│   │   └── alerta.py             # Modelo para validação e serialização de alertas
│   ├── /config                # Configurações do projeto
│   │   └── database.py           # Configuração da conexão com MongoDB
│   └── /routes                # Rotas da API
│       └── alerta_routes.py      # Rotas para criar e listar alertas
├── /tests                     # Testes unitários
│   ├── /unit                  # Testes detalhados por módulo
│   │   ├── test_alerta_repository.py
│   │   ├── test_alerta_service.py
│   │   └── test_rabbitmq_client.py
├── .env                       # Variáveis de ambiente (Twilio, MongoDB, RabbitMQ)
└── requirements.txt           # Dependências Python
```

---

## Instalação

### Pré-requisitos

- **Python 3.8+**
- **Docker e Docker Compose** (para subir MongoDB e RabbitMQ em contêineres)
- **Conta Twilio**: Para envio de notificações via SMS.

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

---

## Configuração do Twilio para Envio de Notificações via SMS

1. Crie uma conta no [Twilio](https://www.twilio.com/).
2. No **Twilio Console**, obtenha o **Account SID** e **Auth Token**.
3. Adicione esses valores no arquivo `.env`:

   ```dotenv
   TWILIO_ACCOUNT_SID=SEU_ACCOUNT_SID
   TWILIO_AUTH_TOKEN=SEU_AUTH_TOKEN
   ```

4. Configure o número `from_` no `notificacao_service.py` para o número fornecido pelo Twilio.

---

```

## Instalação

### Pré-requisitos

- **Python 3.8+**
- **Docker e Docker Compose** (para subir MongoDB e RabbitMQ em contêineres)
- **Conta Twilio**: Para envio de notificações via SMS.

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

## Configuração do Twilio para Envio de Notificações via SMS

1. Crie uma conta no [Twilio](https://www.twilio.com/).
2. No **Twilio Console**, obtenha o **Account SID** e **Auth Token**.
3. Adicione esses valores no arquivo `.env`:

   ```dotenv
   TWILIO_ACCOUNT_SID=SEU_ACCOUNT_SID
   TWILIO_AUTH_TOKEN=SEU_AUTH_TOKEN
   ```

4. Configure o número `from_` no `notificacao_service.py` para o número fornecido pelo Twilio.

## Serviços Principais

### 1. Serviço de Alerta

Para iniciar o serviço que cria alertas e envia mensagens para o **RabbitMQ**, execute o seguinte comando:

```bash
python src/controllers/services/alerta_service.py
```

Este serviço recebe solicitações de criação de alertas e publica mensagens na fila `alertas` do **RabbitMQ**.

### 2. Serviço de Notificações

Para iniciar o serviço que consome as mensagens da fila **RabbitMQ** e envia notificações via SMS usando o Twilio, execute:

```bash
python src/controllers/services/notificacao_service.py
```

Este serviço consome as mensagens de alerta da fila `alertas` e envia notificações para os usuários.

### 3. Serviço de Atualização de Preços

Para rodar o serviço que simula a atualização dos preços dos itens no MongoDB periodicamente, execute o seguinte comando:

```bash
python src/controllers/services/precos_service.py
```

Este serviço atualiza os preços dos itens e armazena o histórico de preços no MongoDB em intervalos de tempo definidos (no exemplo, a cada 10 segundos).

---

## Extensão MongoDB for VS Code

Para facilitar o acesso e gerenciamento do banco de dados MongoDB diretamente no VS Code, você pode instalar a extensão **MongoDB for VS Code**.

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

## Extensão Rabbitrace para RabbitMQ

Para facilitar o monitoramento das filas do RabbitMQ, você pode instalar a extensão **Rabbitrace** no VS Code.

### Instalação da Extensão Rabbitrace

1. Abra o **VS Code**.
2. Acesse o painel de **Extensões** (ícone de quadrado ou `Ctrl+Shift+X`).
3. Na barra de pesquisa, digite **Rabbitrace** e selecione a extensão correspondente.
4. Clique em **Instalar**.

### Configurando a Conexão com RabbitMQ no Rabbitrace

Após a instalação:

1. Abra o **Rabbitrace** na barra lateral.
2. Clique em **New Connection** para adicionar uma nova conexão.
3. Insira as seguintes informações:
   - **Connection Name**: Nome da conexão (ex: `RabbitMQ Local`).
   - **Management API URL**: `http://localhost:15672/api/`
   - **Management API Username**: `guest`
   - **Management API Password**: `guest`
4. Clique em **Save**.

Agora, você deve conseguir visualizar as filas e gerenciar o RabbitMQ diretamente no VS Code.

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
  "produto": "Coxinha",
  "preco_limite": 5.0,
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
    "produto": "Coxinha",
    "preco_limite": 5.0,
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

