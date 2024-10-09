from config.database import get_database
from models.alerta import Alerta

class AlertaRepository:
    def __init__(self):
        self.collection = get_database()["alertas"]

    def salvar_alerta(self, alerta: Alerta):
        # Converte o objeto alerta para dicionário e insere no MongoDB
        self.collection.insert_one(alerta.dict())

    def buscar_todos_alertas(self):
        # Busca todos os documentos da coleção
        return list(self.collection.find())
