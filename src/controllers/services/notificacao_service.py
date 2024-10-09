from integrations.rabbitmq_client import RabbitMQClient

class NotificacaoService:
    def __init__(self):
        self.rabbitmq_client = RabbitMQClient()

    def enviar_notificacao(self, alerta):
        # Aqui você pode implementar envio de notificações (e.g., SMS, email)
        print(f"Notificação enviada para o alerta: {alerta}")

    def iniciar_consumidor(self):
        # Inicia o consumo de alertas no RabbitMQ
        self.rabbitmq_client.consumir_alertas(self.enviar_notificacao)
