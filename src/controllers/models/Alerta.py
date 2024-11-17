from pydantic import BaseModel

class Alerta(BaseModel):
    usuario_id: str
    produto: str
    preco_limite: float
    preco_atual: float
    data_criacao: str
    status: str
    telefone: str  # Número para SMS
