from src.controllers.repositories.alerta_repository import AlertaRepository

class AlertaService:
    def __init__(self):
        self.repository = AlertaRepository()

    def criar_alerta(self, alerta):
        self.repository.salvar_alerta(alerta)

    def listar_alertas(self):
        return self.repository.buscar_alertas_ativos()
