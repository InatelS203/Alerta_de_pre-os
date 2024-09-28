from typing import Optional
from pydantic import BaseModel

class Alerta(BaseModel):
    id: Optional[str]
    usuario_id: str
    produto: str
    preco_limite: float
    data_criacao: Optional[str]
    status: Optional[str]
