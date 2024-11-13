from src.controllers.models.Alerta import Alerta

class AlertFactory:
    @staticmethod
    def criar_alerta(data):
        return Alerta(**data)
