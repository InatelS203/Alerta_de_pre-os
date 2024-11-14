from src.controllers.factories.notification_factory import NotificationFactory
from src.controllers.config.database import Database

def verificar_e_enviar_alertas():
    """
    Função principal para verificar alertas e enviar notificações por SMS.
    """
    alertas = buscar_alertas_ativos()
    sms_notification = NotificationFactory.create_notification('sms')
    
    for alerta in alertas:
        sms_notification.send_notification(alerta)

def buscar_alertas_ativos():
    """
    Função para buscar alertas ativos do banco de dados.
    """
    db = Database().get_collection("alertas")
    return list(db.find({"status": "ativo"}))


# from twilio.rest import Client
# import os

# # Credenciais do Twilio
# account_sid = ""  # Substitua por variáveis de ambiente em produção
# auth_token = ""
# client = Client(account_sid, auth_token)

# def enviar_alerta_whatsapp(alerta):
#     mensagem = f"""
#     Alerta de Preço:
#     Produto: {alerta['produto']}
#     Preço Limite: {alerta['preco_limite']}
#     Status: {alerta['status']}
#     """
#     try:
#         message = client.messages.create(
#             from_="+",  # Número do Twilio Sandbox para WhatsApp
#             body=mensagem,
#             to="+",  # Substitua pelo número de destino com o código do país
#         )
#         print(f"Mensagem enviada com sucesso. SID: {message.sid}")
#     except Exception as e:
#         print(f"Erro ao enviar mensagem: {e}")


# def verificar_e_enviar_alertas():
#     """
#     Função principal para verificar alertas e enviar notificações por SMS.
#     """
#     alertas = buscar_alertas_ativos()  # Função que busca alertas ativos no banco de dados
#     for alerta in alertas:
#         enviar_alerta_whatsapp(alerta)

# # Função para buscar alertas ativos
# def buscar_alertas_ativos():
#     """
#     Função de exemplo para simular a busca de alertas ativos.
#     Em uma implementação real, esta função deve buscar alertas ativos no banco de dados.
#     """
#     return [
#         {
#             "produto": "Coxinha",
#             "preco_limite": 4.0,
#             "status": "ativo",
#             "telefone": "+"  # Número de destino para SMS
#         },
#         {
#             "produto": "Refrigerante",
#             "preco_limite": 5.0,
#             "status": "ativo",
#             "telefone": "+"  # Número de destino para SMS
#         }
#     ]

# # Executar a verificação e envio de alertas
# verificar_e_enviar_alertas()