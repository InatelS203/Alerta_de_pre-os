from integrations.rabbitmq_client import RabbitMQClient

class NotificacaoService:
    def __init__(self):
        self.rabbitmq_client = RabbitMQClient()

    def enviar_notificacao(self, alerta):
        # Aqui você enviaria uma notificação por email ou SMS
        print(f"Notificação enviada para o alerta: {alerta}")

    def iniciar_consumidor(self):
        self.rabbitmq_client.consumir_alertas(self.enviar_notificacao)
