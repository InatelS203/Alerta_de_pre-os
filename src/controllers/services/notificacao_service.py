#!/usr/bin/env python
import pika, sys, os, json

def main():
    # Conectar ao RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declarar a fila 'alertas'
    channel.queue_declare(queue='alertas')

    # Função callback que processa a mensagem recebida
    def callback(ch, method, properties, body):
        alerta = json.loads(body)  # Converte a mensagem recebida de JSON para um dicionário
        print(f" [x] Alerta Recebido: Produto: {alerta['produto']}, Preço Limite: {alerta['preco_limite']}, Status: {alerta['status']}")

    # Consumir mensagens da fila 'alertas'
    channel.basic_consume(queue='alertas', on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens. Para sair, pressione CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Processo interrompido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
