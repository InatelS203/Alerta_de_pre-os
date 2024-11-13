from twilio.rest import Client
import os


class NotificationStrategy:
    def send_notification(self, alerta):
        raise NotImplementedError("Essa função precisa ser implementada.")


class SMSNotification(NotificationStrategy):
    def __init__(self):
        # Configure as credenciais do Twilio
        self.account_sid = ""
        self.auth_token = ""
        self.client = Client(self.account_sid, self.auth_token)

    def send_notification(self, alerta):
        # Implementação para enviar SMS
        mensagem = f"Alerta de Preço para {alerta['produto']}: Preço Limite {alerta['preco_limite']}"
        try:
            message = self.client.messages.create(
                from_="",  # Número de origem do Twilio
                body=mensagem,
                to=alerta["telefone"],  # Número de telefone do usuário
            )
            print(f"SMS enviado com sucesso. SID: {message.sid}")
        except Exception as e:
            print(f"Erro ao enviar SMS: {e}")
