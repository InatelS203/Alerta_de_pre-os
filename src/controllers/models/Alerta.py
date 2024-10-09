from pydantic import BaseModel

class Alerta(BaseModel):
    usuario_id: str
    produto: str
    preco_limite: float
    data_criacao: str
    status: str
