from repositories.alerta_repository import AlertaRepository

class AlertaService:
    def __init__(self):
        self.alerta_repository = AlertaRepository()

    def criar_alerta(self, dados):
        # Lógica para criar alerta
        alerta = self.alerta_repository.salvar_alerta(dados)
        return alerta

    def listar_alertas(self):
        # Lógica para listar alertas
        return self.alerta_repository.buscar_todos_alertas()
