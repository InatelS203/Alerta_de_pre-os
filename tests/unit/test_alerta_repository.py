from repositories.alerta_repository import AlertaRepository
from models.alerta import Alerta
from unittest.mock import MagicMock


def test_salvar_alerta():
    mock_collection = MagicMock()

    repository = AlertaRepository()
    repository.collection = mock_collection

    alerta = Alerta(usuario_id="123", produto="Produto X", preco_limite=100.0, data_criacao="2024-09-02",
                    status="ativo")

    repository.salvar_alerta(alerta)

    mock_collection.insert_one.assert_called_once_with(alerta.dict())


def test_buscar_todos_alertas():
    mock_collection = MagicMock()

    mock_collection.find.return_value = [
        {"usuario_id": "123", "produto": "Produto X", "preco_limite": 100.0, "data_criacao": "2024-09-02",
         "status": "ativo"},
        {"usuario_id": "456", "produto": "Produto Y", "preco_limite": 200.0, "data_criacao": "2024-09-03",
         "status": "ativo"}
    ]

    repository = AlertaRepository()
    repository.collection = mock_collection

    alertas = repository.buscar_todos_alertas()

    mock_collection.find.assert_called_once()
    assert len(alertas) == 2
    assert alertas[0]["produto"] == "Produto X"
    assert alertas[1]["produto"] == "Produto Y"
