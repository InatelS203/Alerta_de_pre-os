class NotificationStrategy:
    def send_notification(self, alerta):
        raise NotImplementedError("Método não implementado.")

class SMSNotification(NotificationStrategy):
    def __init__(self, client):
        self.client = client

    def send_notification(self, alerta):
        mensagem = f"Alerta de Preço: {alerta['produto']} custa agora R${alerta['preco_atual']}!"
        try:
            message = self.client.messages.create(
                from_="+12164555265",  # Número Twilio
                body=mensagem,
                to=alerta["telefone"]
            )
            print(f"SMS enviado com sucesso para {alerta['telefone']}. SID: {message.sid}")
        except Exception as e:
            print(f"Erro ao enviar SMS: {e}")
