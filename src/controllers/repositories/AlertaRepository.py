from pymongo import MongoClient

class AlertaRepository:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['alertas_db']
        self.collection = self.db['alertas']

    def salvar_alerta(self, dados):
        # Salvando o alerta no MongoDB
        result = self.collection.insert_one(dados)
        return result.inserted_id

    def buscar_todos_alertas(self):
        # Retorna todos os alertas do banco de dados
        return list(self.collection.find())
