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
│   ├── /controllers        
│   │   └── alerta_controller.py
│   ├── /services           # Lógica de negócios, comunicação com repositórios e RabbitMQ
│   │   ├── alerta_service.py
│   │   ├── notificacao_service.py  # Serviço de notificação de alerta
│   │   └── precos_service.py  # Serviço de atualização de preços
│   ├── /repositories       
│   │   └── alerta_repository.py
│   ├── /integrations       
│   │   └── rabbitmq_client.py
│   ├── /models             
│   │   └── alerta.py
│   ├── /config             
│   │   └── database.py
│   └── /routes             
│       └── alerta_routes.py
├── /tests                  
│   ├── /unit               
│   │   ├── test_alerta_repository.py
│   │   ├── test_alerta_service.py
│   │   └── test_rabbitmq_client.py
├── .env                    
├── requirements.txt        
└── docker-compose.yml      
```

## Instalação do RabbitMQ

### 1. Instalar RabbitMQ

Para instalar o **RabbitMQ** no seu sistema, siga os passos abaixo:

#### **Windows**:
1. Faça o download do **RabbitMQ Installer** no site oficial:  
   [https://www.rabbitmq.com/install-windows.html](https://www.rabbitmq.com/install-windows.html)
2. Siga as instruções de instalação no site, que incluem também a instalação do **Erlang** (prérequisito para o RabbitMQ).

#### **Linux**:
1. No terminal, instale o RabbitMQ com o seguinte comando:
   
   ```bash
   sudo apt-get install rabbitmq-server
   ```

2. Após a instalação, inicie o RabbitMQ:

   ```bash
   sudo service rabbitmq-server start
   ```

### 2. Habilitar o RabbitMQ Management Plugin

Após instalar o **RabbitMQ**, é necessário habilitar o **RabbitMQ Management Plugin** para acessar a interface de gerenciamento web.

1. **Habilitar o plugin de gerenciamento**:

   No terminal, execute o seguinte comando para habilitar o plugin:

   ```bash
   rabbitmq-plugins enable rabbitmq_management
   ```

2. **Reiniciar o RabbitMQ**:
   
   As mudanças só terão efeito após reiniciar o RabbitMQ. Execute os comandos abaixo para reiniciar o RabbitMQ:

   ```bash
   rabbitmqctl stop
   rabbitmq-server
   ```

### 3. Acessar o Gerenciador Web do RabbitMQ

Para verificar e gerenciar as filas e exchanges do RabbitMQ, você pode acessar o painel de gerenciamento web do RabbitMQ.

1. Abra um navegador web e digite o seguinte URL:

   ```
   http://localhost:15672
   ```

2. Ao acessar o painel de gerenciamento, você precisará fornecer as credenciais padrão de acesso:

   - **Usuário**: `guest`
   - **Senha**: `guest`

Agora você pode visualizar e gerenciar as filas, exchanges e verificar o status do RabbitMQ diretamente através da interface web.

---

## Rodar os Serviços

### 1. Executar o Serviço de Alerta

Para iniciar o serviço que cria alertas e envia mensagens para o **RabbitMQ**, execute o seguinte comando:

```bash
python src/controllers/services/alerta_service.py
```

Este serviço recebe solicitações de criação de alertas e publica mensagens na fila `alertas` do **RabbitMQ**.

### 2. Executar o Serviço de Notificações

Para iniciar o serviço que consome as mensagens da fila **RabbitMQ** e envia notificações por email, execute:

```bash
python src/controllers/services/notificacao_service.py
```

Este serviço consome as mensagens de alerta da fila `alertas` e envia notificações (como emails) para os usuários.

### 3. Executar o Serviço de Atualização de Preços

Para rodar o serviço que simula a atualização dos preços dos itens no MongoDB de forma periódica, execute o seguinte comando:

```bash
python src/controllers/services/precos_service.py
```

Este serviço atualiza os preços dos itens e armazena o histórico de preços no MongoDB. Ele está configurado para rodar em intervalos de tempo específicos (no exemplo, a cada 10 segundos).

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

---

Agora o **README.md** está atualizado com as instruções para rodar os três principais serviços:
1. **Serviço de Alerta** para criação de alertas.
2. **Serviço de Notificação** para envio de alertas por email.
3. **Serviço de Atualização de Preços** para atualização periódica dos preços no MongoDB.