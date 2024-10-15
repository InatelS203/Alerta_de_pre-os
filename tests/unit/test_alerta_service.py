import unittest
from unittest.mock import MagicMock
from src.controllers.services.alerta_service import AlertaService
from src.controllers.models.Alerta import Alerta

class TestAlertaService(unittest.TestCase):

    def setUp(self):
        # Mockando o repositório e o RabbitMQ client
        self.mock_repository = MagicMock()
        self.mock_rabbitmq = MagicMock()
        self.alerta_service = AlertaService(self.mock_repository, self.mock_rabbitmq)

    def test_criar_alerta(self):
        alerta = Alerta(usuario_id="123", produto="Produto X", preco_limite=100.0, data_criacao="2024-09-02", status="ativo")
        
        self.alerta_service.criar_alerta(alerta)
        
        # Verifica se o alerta foi salvo e enviado para RabbitMQ
        self.mock_repository.salvar_alerta.assert_called_once_with(alerta)
        self.mock_rabbitmq.publicar_alerta.assert_called_once_with(str(alerta))

    def test_listar_alertas(self):
        self.mock_repository.buscar_todos_alertas.return_value = [
            {"usuario_id": "123", "produto": "Produto X", "preco_limite": 100.0, "data_criacao": "2024-09-02", "status": "ativo"},
            {"usuario_id": "456", "produto": "Produto Y", "preco_limite": 200.0, "data_criacao": "2024-09-03", "status": "ativo"}
        ]
        
        alertas = self.alerta_service.listar_alertas()
        
        self.mock_repository.buscar_todos_alertas.assert_called_once()
        self.assertEqual(len(alertas), 2)
        self.assertEqual(alertas[0]["produto"], "Produto X")
        self.assertEqual(alertas[1]["produto"], "Produto Y")

if __name__ == '__main__':
    unittest.main()
