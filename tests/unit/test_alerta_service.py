import pytest
from services.alerta_service import AlertaService
from models.alerta import Alerta


# Mock da repository e RabbitMQ Client
class MockAlertaRepository:
    def __init__(self):
        self.alertas = []

    def salvar_alerta(self, alerta):
        self.alertas.append(alerta)

    def buscar_todos_alertas(self):
        return self.alertas


class MockRabbitMQClient:
    def __init__(self):
        self.mensagens = []

    def publicar_alerta(self, mensagem):
        self.mensagens.append(mensagem)


@pytest.fixture
def alerta_service():
    # Usando mocks no lugar de classes reais
    mock_repository = MockAlertaRepository()
    mock_rabbitmq = MockRabbitMQClient()
    return AlertaService(mock_repository, mock_rabbitmq)


def test_criar_alerta(alerta_service):
    alerta = Alerta(usuario_id="123", produto="Produto X", preco_limite=100.0, data_criacao="2024-09-02",
                    status="ativo")

    alerta_service.criar_alerta(alerta)

    assert len(alerta_service.alerta_repository.alertas) == 1
    assert alerta_service.alerta_repository.alertas[0].produto == "Produto X"
    assert len(alerta_service.rabbitmq_client.mensagens) == 1


def test_listar_alertas(alerta_service):
    alerta1 = Alerta(usuario_id="123", produto="Produto X", preco_limite=100.0, data_criacao="2024-09-02",
                     status="ativo")
    alerta2 = Alerta(usuario_id="456", produto="Produto Y", preco_limite=200.0, data_criacao="2024-09-03",
                     status="ativo")

    alerta_service.criar_alerta(alerta1)
    alerta_service.criar_alerta(alerta2)

    alertas = alerta_service.listar_alertas()

    assert len(alertas) == 2
    assert alertas[0].produto == "Produto X"
    assert alertas[1].produto == "Produto Y"
