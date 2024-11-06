from twilio.rest import Client
import os

# Credenciais do Twilio
account_sid = "AC"
auth_token = ""
client = Client(account_sid, auth_token)


def enviar_alerta_whatsapp(alerta):
    mensagem = f"""
    Alerta de Preço:
    Produto: {alerta['produto']}
    Preço Limite: {alerta['preco_limite']}
    Status: {alerta['status']}
    """
    try:
        message = client.messages.create(
            from_="+",  # Número do Twilio Sandbox para WhatsApp
            body=mensagem,
            to="+",  # Substitua pelo número de destino com o código do país
        )
        print(f"Mensagem enviada com sucesso. SID: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")


# Exemplo de alerta
alerta = {
    "produto": "Coxinha",
    "preco_limite": 4.0,
    "status": "ativo"
}

enviar_alerta_whatsapp(alerta)
