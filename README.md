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
python src.controllers.services.alerta_service.py
```

Este serviço recebe solicitações de criação de alertas e publica mensagens na fila `alertas` do **RabbitMQ**.

### 2. Serviço de Notificações

Para iniciar o serviço que consome as mensagens da fila **RabbitMQ** e envia notificações via SMS usando o Twilio, execute:

```bash
python src.controllers.services.notificacao_service.py
```

Este serviço consome as mensagens de alerta da fila `alertas` e envia notificações para os usuários.

### 3. Serviço de Atualização de Preços

Para rodar o serviço que simula a atualização dos preços dos itens no MongoDB periodicamente, execute o seguinte comando:

```bash
python src.controllers.services.precos_service.py
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


---
# Explicação sobre as UMLs com Design Patterns

### **Descrição Geral do Fluxo diagrama de Sequência com Design Patterns**

1. O serviço de notificação (`NotificacaoService`) executa o processo de **monitoramento de preços** utilizando um loop de *polling*.
2. Para cada **alerta ativo** encontrado no banco de dados (`MongoDB`), o sistema verifica se o preço atual do produto é menor ou igual ao limite definido.
3. Se o preço atingiu a condição de notificação, o sistema utiliza o **Factory Pattern** para instanciar a estratégia de notificação (`SMSNotification`).
4. A estratégia **SMSNotification** envia a mensagem de alerta via **Twilio API**.
5. A interação finaliza com a confirmação de que a notificação foi enviada com sucesso.

---

### **Explicação do diagrama de Sequência com Design Patterns **

1. **Usuário Inicializa o Monitoramento**:
   - O **usuário** ou o sistema inicia o monitoramento contínuo dos alertas executando o `NotificacaoService`.

2. **Consulta de Alertas Ativos**:
   - O **`NotificacaoService`** consulta o **MongoDB** para obter todos os alertas com status ativo.

3. **Consulta do Preço Atual**:
   - Para cada alerta ativo, o sistema consulta o preço atual do produto na coleção de preços do **MongoDB**.

4. **Verificação da Condição de Notificação**:
   - O serviço verifica se o preço atual do produto é menor ou igual ao preço limite definido no alerta.

5. **Fábrica de Notificações**:
   - Se a condição for atendida, o serviço usa o **Factory Pattern** (`NotificationFactory`) para instanciar a estratégia de notificação (`SMSNotification`).

6. **Envio da Notificação**:
   - A estratégia `SMSNotification` é responsável por enviar a notificação via **Twilio API**.

7. **Confirmação de Envio**:
   - O Twilio retorna a confirmação de que o SMS foi enviado com sucesso.

8. **Não Envia Notificação**:
   - Caso o preço ainda esteja acima do limite, o sistema não envia a notificação.

---

### **Design Patterns no Fluxo**

1. **Singleton Pattern**:
   - Implementação utiliza o envio de SMS como estratégia padrão.
   - Permitir a inclusão futura de novos métodos de notificação (ex.: e-mail, WhatsApp) sem alterar a lógica principal.

2. **Strategy Pattern**:
   - Abstrai o envio da notificação, permitindo diferentes estratégias para envio.
   - A estratégia **`SMSNotification`** implementa o envio de notificações via SMS.

3. **Repository Pattern**:
   - O `NotificacaoService` interage com o **MongoDB** por meio do **`AlertaRepository`**, encapsulando as operações de banco de dados.

4. **Observer Pattern**:
   - Embora neste sistema o monitoramento seja feito por *polling*, ele atua como uma implementação indireta do padrão **Observer**: o serviço observa mudanças no estado dos alertas e toma ações específicas.

---

### **Resumo**
Este diagrama de sequência e a explicação detalham como o sistema implementa **design patterns** para alcançar modularidade, facilidade de manutenção e extensibilidade.

---
### **UML comportamental com design patterns**
---

### **Visão Geral do Fluxo**
O diagrama ilustra como o sistema gerencia notificações de alertas, interagindo com serviços externos, bancos de dados e sistemas de mensagens. Ele é organizado em **três fluxos principais** que se integram:

1. **Recepção e Processamento de Notificações.**
2. **Atualização de Preços.**
3. **Criação e Persistência de Alertas.**

A seguir, explico o fluxo, com destaque aos padrões de design.

---

### **1. Recepção e Processamento de Notificações**
#### **Descrição do Fluxo:**
- O processo começa com o **Usuário** acionando o sistema.
- A etapa inicial é "Receber Notificação", onde as notificações de alterações ou eventos são captadas.
- Em seguida, a notificação é processada:
  - Aqui, entra o **Strategy Pattern**, encapsulando a lógica de envio de notificações.
  - A classe base `NotificationStrategy` define um contrato, enquanto a implementação concreta `SMSNotification` cuida do envio de notificações via SMS. Isso permite que no futuro seja fácil adicionar novas formas de notificação (e.g., e-mail, WhatsApp).
- O envio final da notificação é realizado pela classe `NotificacaoService`.

---

### **2. Atualização de Preços**
#### **Descrição do Fluxo:**
- A partir de uma interação com um **Sistema Externo**, o sistema busca dados de preços.
- O sistema atualiza os preços:
  - Ele consulta uma API de preços e atualiza o banco de dados.
- Esse fluxo ilustra a conexão entre o sistema de monitoramento e os dados armazenados.

---

### **3. Criação e Persistência de Alertas**
#### **Descrição do Fluxo:**
- O **Usuário** solicita a criação de um alerta no sistema.
- O sistema segue os passos abaixo:
  1. **Criação do Alerta:** Um alerta é criado no serviço principal.
  2. **Persistência no Banco de Dados:** O alerta é salvo no MongoDB.
     - Aqui, entra o **Repository Pattern**, com a classe `AlertaRepository` intermediando o acesso ao banco.
     - Essa separação permite que a lógica de acesso ao banco de dados seja isolada, facilitando a troca do banco no futuro (e.g., de MongoDB para MySQL).
  3. **Envio para RabbitMQ:** O alerta também é publicado em uma fila no RabbitMQ, garantindo comunicação assíncrona com outros serviços.

---

### **Padrões de Design Detalhados**

#### **1. Strategy Pattern**
- Local: Encapsulado na lógica de envio de notificações.
- Classes Relacionadas:
  - `NotificationStrategy`: Interface para diferentes estratégias.
  - `SMSNotification`: Implementação concreta que envia notificações via SMS.
- Benefício: Permite adicionar novas formas de envio sem alterar o código existente.

#### **2. Singleton Pattern**
- Local: Implementado na conexão com o MongoDB.
- Classe Relacionada: `MongoClient`.
- Lógica:
  - Apenas uma instância de `MongoClient` é criada e compartilhada.
- Benefício: Garante uma única conexão ao banco, otimizando recursos.

#### **3. Repository Pattern**
- Local: Intermediando o acesso ao MongoDB.
- Classe Relacionada: `AlertaRepository`.
- Lógica:
  - A lógica de acesso ao banco é separada da lógica de negócio.
- Benefício: Facilita manutenção e trocas de tecnologia no futuro.

---

### **Resumo do Fluxo**
- O sistema começa com notificações ou solicitações de criação de alertas.
- Envia notificações utilizando estratégias flexíveis (Strategy).
- Atualiza os preços ao consultar serviços externos.
- Persiste dados no banco através de repositórios (Repository) e garante conexões otimizadas (Singleton).

O diagrama atualizado mencionado é um **Diagrama Estrutural** que reflete as classes, seus relacionamentos, e a implementação dos padrões de design **Strategy**, **Singleton** e **Repository** no contexto do sistema de monitoramento e notificações. Vou detalhar como cada padrão foi integrado e como os componentes interagem.

---
### ** UML estrutural com design patternsUML estrutural com design patterns**

### **1. Strategy Pattern**
#### **Descrição:**
O **Strategy Pattern** é implementado para permitir diferentes formas de envio de notificações, como SMS, e-mail, ou WhatsApp. A ideia é encapsular a lógica de envio em classes específicas, mantendo a flexibilidade de trocar ou adicionar novas estratégias sem alterar o código principal.

#### **Componentes no Diagrama:**
- **Classe Base:** `NotificationStrategy` define a interface padrão para envio de notificações.
- **Implementação Concreta:** 
  - `SMSNotification` implementa o envio via SMS como a estratégia atual.
- **Serviço:** A classe `AlertaService` utiliza o `NotificationStrategy` para enviar notificações. A dependência da estratégia é injetada, garantindo flexibilidade.

#### **Vantagens:**
- Adicionar novos métodos de envio (e.g., e-mail) se torna simples.
- Evita modificações em serviços centrais como o `AlertaService`.

#### **Exemplo no Fluxo:**
- Quando um alerta é criado e precisa ser notificado ao usuário, o serviço utiliza a estratégia `SMSNotification` para envio via SMS.

---

### **2. Singleton Pattern**
#### **Descrição:**
O **Singleton Pattern** é usado para gerenciar a conexão com o banco de dados MongoDB. Ele garante que apenas uma instância de conexão seja criada e reutilizada em todo o sistema.

#### **Componentes no Diagrama:**
- **Classe:** `MongoClient` representa a conexão única ao banco de dados.
- **Método de Acesso:** Um método (como `get_instance()` ou `get_database()`) assegura que a instância única do cliente MongoDB seja compartilhada.

#### **Vantagens:**
- Reduz custos computacionais ao evitar múltiplas conexões ao banco.
- Simplifica a reutilização da conexão em diferentes partes do sistema.

#### **Exemplo no Fluxo:**
- Sempre que um alerta precisa ser salvo ou lido do MongoDB, o serviço `AlertaRepository` utiliza a mesma instância de `MongoClient`.

---

### **3. Repository Pattern**
#### **Descrição:**
O **Repository Pattern** é usado para encapsular o acesso ao banco de dados, separando a lógica de persistência da lógica de negócios. Isso torna o sistema mais modular e facilita a troca do banco de dados, se necessário.

#### **Componentes no Diagrama:**
- **Classe:** `AlertaRepository` encapsula as operações com o banco de dados.
- **Métodos:**
  - `salvar_alerta()`: Para salvar alertas no MongoDB.
  - `buscar_alertas_ativos()`: Para recuperar alertas ativos.
- **Serviço Relacionado:** `AlertaService` utiliza o `AlertaRepository` para acessar os dados.

#### **Vantagens:**
- A lógica de persistência está centralizada e desacoplada de outros serviços.
- Alterar o banco de dados (e.g., migrar de MongoDB para MySQL) requer apenas mudanças no repositório.

#### **Exemplo no Fluxo:**
- Quando um novo alerta é criado, o `AlertaService` chama o método `salvar_alerta()` do `AlertaRepository` para persistir os dados.

---



