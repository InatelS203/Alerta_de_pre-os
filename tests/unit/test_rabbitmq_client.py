import unittest
from unittest.mock import MagicMock
from src.controllers.integrations.rabbitmq_client import RabbitMQClient

class TestRabbitMQClient(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para cada teste
        self.mock_channel = MagicMock()
        self.rabbitmq_client = RabbitMQClient()
        self.rabbitmq_client.channel = self.mock_channel

    def test_publicar_alerta(self):
        mensagem = "Alerta de teste"
        self.rabbitmq_client.publicar_alerta(mensagem)
        
        # Verifica se o método basic_publish foi chamado corretamente
        self.mock_channel.basic_publish.assert_called_once_with(exchange='', routing_key='alertas', body=mensagem)

if __name__ == '__main__':
    unittest.main()
