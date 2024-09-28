import pika


class RabbitMQClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="alertas")

    def publicar_alerta(self, mensagem):
        self.channel.basic_publish(exchange='', routing_key='alertas', body=mensagem)

    def consumir_alertas(self, callback):
        def _callback(ch, method, properties, body):
            callback(body)

        self.channel.basic_consume(queue='alertas', on_message_callback=_callback, auto_ack=True)
        self.channel.start_consuming()
