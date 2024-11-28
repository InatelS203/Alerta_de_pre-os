# from src.controllers.repositories.alerta_repository import AlertaRepository

# class AlertaService:
#     def __init__(self):
#         self.repository = AlertaRepository()

#     def criar_alerta(self, alerta):
#         self.repository.salvar_alerta(alerta)

#     def listar_alertas(self):
#         return self.repository.buscar_alertas_ativos()


#!/usr/bin/env python
import pika
import json

# Configuração de conexão com o RabbitMQ
rabbitmq_host = 'localhost'
rabbitmq_port = 5672  # Porta padrão do RabbitMQ
rabbitmq_user = 'guest'  # Substitua pelo usuário do RabbitMQ
rabbitmq_password = 'guest'  # Substitua pela senha do usuário

# Conectar ao RabbitMQ com credenciais
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=credentials
    )
)
channel = connection.channel()

# Declarar a fila 'alertas' no RabbitMQ
channel.queue_declare(queue='alertas')

# Exemplo de alerta de preço
alerta = {
    "usuario_id": "123",
    "produto": "Coxinha",               # Nome do item da cantina
    "preco_limite": 4.0,                # Limite de preço para notificação
    "preco_atual": 4.5,                 # Preço atual do item
    "data_criacao": "2024-09-02T12:00:00",  # Data de criação do alerta
    "status": "ativo"                   # Status do alerta
}

# Converter o alerta para o formato JSON antes de enviar
mensagem = json.dumps(alerta)

# Publicar a mensagem na fila 'alertas'
channel.basic_publish(exchange='', routing_key='alertas', body=mensagem)

print(f" [x] Alerta enviado: {mensagem}")

# Fechar a conexão
connection.close()
