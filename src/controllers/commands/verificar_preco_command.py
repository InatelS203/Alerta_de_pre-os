class VerificarPrecoCommand:
    def __init__(self, alerta_service):
        self.alerta_service = alerta_service

    def execute(self):
        self.alerta_service.verificar_precos()
