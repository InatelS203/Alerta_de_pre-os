from fastapi import APIRouter, HTTPException
from src.controllers.services.notificacao_service import verificar_e_enviar_alertas
from src.controllers.models.Alerta import Alerta
from src.controllers.services.alerta_service import AlertaService

router = APIRouter()
alerta_service = AlertaService()

@router.post("/alertas")
def criar_alerta(alerta: Alerta):
    try:
        alerta_service.criar_alerta(alerta)
        verificar_e_enviar_alertas()  # Acionar a verificação e envio de notificações
        return {"message": "Alerta criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alertas")
def listar_alertas():
    try:
        return alerta_service.listar_alertas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
