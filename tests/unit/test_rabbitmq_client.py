from integrations.rabbitmq_client import RabbitMQClient
from unittest.mock import MagicMock

def test_publicar_alerta():
    mock_channel = MagicMock()
    client = RabbitMQClient()
    client.channel = mock_channel
    mensagem = "Alerta de teste"
    client.publicar_alerta(mensagem)
    mock_channel.basic_publish.assert_called_once_with(exchange='', routing_key='alertas', body=mensagem)
