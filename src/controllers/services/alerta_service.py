from repositories.alerta_repository import AlertaRepository
from integrations.rabbitmq_client.py import RabbitMQClient

class AlertaService:
    def __init__(self):
        self.alerta_repository = AlertaRepository()
        self.rabbitmq_client = RabbitMQClient()

    def criar_alerta(self, alerta_dados):
        # Salva alerta no banco de dados
        self.alerta_repository.salvar_alerta(alerta_dados)

        # Publica alerta na fila RabbitMQ para processar posteriormente
        self.rabbitmq_client.publicar_alerta(str(alerta_dados))

    def listar_alertas(self):
        return self.alerta_repository.buscar_todos_alertas()
