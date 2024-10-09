from repositories.alerta_repository import AlertaRepository
from integrations.rabbitmq_client import RabbitMQClient
from models.alerta import Alerta

class AlertaService:
    def __init__(self):
        self.alerta_repository = AlertaRepository()
        self.rabbitmq_client = RabbitMQClient()

    def criar_alerta(self, alerta: Alerta):
        # Salva o alerta no MongoDB
        self.alerta_repository.salvar_alerta(alerta)

        # Envia o alerta para RabbitMQ
        self.rabbitmq_client.publicar_alerta(str(alerta))

    def listar_alertas(self):
        # Retorna todos os alertas do MongoDB
        return self.alerta_repository.buscar_todos_alertas()
