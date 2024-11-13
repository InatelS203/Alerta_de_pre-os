from src.controllers.services.notificacao_service import SMSNotification

# Inicializa a estratégia de SMS
sms_notifier = SMSNotification()

def verificar_e_enviar_alertas():
    """
    Função principal para verificar alertas e enviar notificações por SMS.
    """
    alertas = buscar_alertas_ativos()  # Função que busca alertas ativos no banco de dados
    for alerta in alertas:
        sms_notifier.send_notification(alerta)  # Envia o SMS usando a estratégia

# Função para buscar alertas ativos
def buscar_alertas_ativos():
    """
    Função de exemplo para simular a busca de alertas ativos.
    Em uma implementação real, esta função deve buscar alertas ativos no banco de dados.
    """
    return [
        {
            "produto": "Coxinha",
            "preco_limite": 4.0,
            "status": "ativo",
            "telefone": "+"  # Número de destino para SMS
        },
        {
            "produto": "Refrigerante",
            "preco_limite": 5.0,
            "status": "ativo",
            "telefone": "+"  # Número de destino para SMS
        }
    ]

# Executar a verificação e envio de alertas
if __name__ == "__main__":
    verificar_e_enviar_alertas()