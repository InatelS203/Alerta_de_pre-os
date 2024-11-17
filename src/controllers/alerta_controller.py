from src.controllers.services.alerta_service import AlertaService
from src.controllers.models.Alerta import Alerta

alerta_service = AlertaService()

def criar_alerta(alerta: Alerta):
    alerta_service.criar_alerta(alerta)
    print("Alerta criado com sucesso.")

def listar_alertas():
    return alerta_service.listar_alertas()
