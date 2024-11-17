from src.controllers.services.notificacao_service import NotificacaoService

def iniciar_servico_verificacao():
    """
    Inicia o serviço de verificação de alertas periodicamente.
    """
    notificacao_service = NotificacaoService(usar_simulacao=True)  # Alterar para False para usar dados reais

    while True:
        notificacao_service.verificar_e_enviar_alertas()
        print("Verificação de alertas concluída. Aguardando 10 segundos para nova verificação.")
        time.sleep(10)  # Intervalo de verificação em segundos

if __name__ == "__main__":
    iniciar_servico_verificacao()
