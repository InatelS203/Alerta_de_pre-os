from fastapi import APIRouter, HTTPException
from services.alerta_service import AlertaService
from models.alerta import Alerta

router = APIRouter()
alerta_service = AlertaService()

@router.post("/alertas")
def criar_alerta(alerta: Alerta):
    try:
        alerta_service.criar_alerta(alerta)
        return {"message": "Alerta criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alertas")
def listar_alertas():
    try:
        return alerta_service.listar_alertas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
