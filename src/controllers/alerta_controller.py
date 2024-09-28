from fastapi import APIRouter
from services.alerta_service import AlertaService
from models.alerta import Alerta

router = APIRouter()
alerta_service = AlertaService()

@router.post("/alertas")
def criar_alerta(alerta: Alerta):
    alerta_service.criar_alerta(alerta)
    return {"message": "Alerta criado com sucesso!"}

@router.get("/alertas")
def listar_alertas():
    return alerta_service.listar_alertas()
