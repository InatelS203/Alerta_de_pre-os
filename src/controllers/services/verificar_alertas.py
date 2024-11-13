import time
from src.controllers.services.notificacao_service import verificar_e_enviar_alertas

def iniciar_servico_verificacao():
    while True:
        verificar_e_enviar_alertas()
        print("Verificação de alertas concluída. Aguardando 10 segundos para nova verificação.")
        time.sleep(10)  # Intervalo de verificação em segundos

if __name__ == "__main__":
    iniciar_servico_verificacao()
