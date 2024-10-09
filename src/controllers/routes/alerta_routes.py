from fastapi import FastAPI
from controllers.alerta_controller import router as alerta_router

app = FastAPI()

# Inclui as rotas da API de alertas
app.include_router(alerta_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
