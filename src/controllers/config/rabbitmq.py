import pika

class RabbitMQ:
    _connection = None

    @staticmethod
    def get_connection():
        if RabbitMQ._connection is None:
            RabbitMQ._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="localhost")
            )
        return RabbitMQ._connection
