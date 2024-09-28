from pymongo.collection import Collection
from models.alerta import Alerta
from config.database import get_database

class AlertaRepository:
    def __init__(self):
        self.collection: Collection = get_database()["alertas"]

    def salvar_alerta(self, alerta: Alerta):
        self.collection.insert_one(alerta.dict())

    def buscar_todos_alertas(self):
        return list(self.collection.find())
