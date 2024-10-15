import unittest
from unittest.mock import MagicMock
from src.controllers.repositories.alerta_repository import AlertaRepository
from src.controllers.models.Alerta import Alerta

class TestAlertaRepository(unittest.TestCase):

    def setUp(self):
        # Cria um mock da coleção do MongoDB
        self.mock_collection = MagicMock()
        self.repository = AlertaRepository()
        self.repository.collection = self.mock_collection

    def test_salvar_alerta(self):
        alerta = Alerta(usuario_id="123", produto="Produto X", preco_limite=100.0, data_criacao="2024-09-02", status="ativo")
        
        self.repository.salvar_alerta(alerta)
        
        # Verifica se o método insert_one foi chamado corretamente
        self.mock_collection.insert_one.assert_called_once_with(alerta.dict())

    def test_buscar_todos_alertas(self):
        self.mock_collection.find.return_value = [
            {"usuario_id": "123", "produto": "Produto X", "preco_limite": 100.0, "data_criacao": "2024-09-02", "status": "ativo"},
            {"usuario_id": "456", "produto": "Produto Y", "preco_limite": 200.0, "data_criacao": "2024-09-03", "status": "ativo"}
        ]
        
        alertas = self.repository.buscar_todos_alertas()
        
        self.mock_collection.find.assert_called_once()
        self.assertEqual(len(alertas), 2)
        self.assertEqual(alertas[0]["produto"], "Produto X")
        self.assertEqual(alertas[1]["produto"], "Produto Y")

if __name__ == '__main__':
    unittest.main()
