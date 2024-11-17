from src.controllers.config.database import get_database

class AlertaRepository:
    def __init__(self):
        self.collection = get_database()["alertas"]

    def salvar_alerta(self, alerta):
        """
        Salva um alerta no banco de dados.
        """
        self.collection.insert_one(alerta.dict())

    def buscar_alertas_ativos(self):
        """
        Busca todos os alertas com status 'ativo' no banco de dados.
        """
        return list(self.collection.find({"status": "ativo"}))
