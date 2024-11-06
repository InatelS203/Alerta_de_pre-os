#!/usr/bin/env python
import pika
import json

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
