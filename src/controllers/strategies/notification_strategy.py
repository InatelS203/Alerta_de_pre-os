class NotificationStrategy:
    def send_notification(self, alerta):
        raise NotImplementedError("Este método precisa ser implementado nas subclasses")


class SMSNotification(NotificationStrategy):
    def send_notification(self, alerta):
        from twilio.rest import Client

        account_sid = ""
        auth_token = ""
        client = Client(account_sid, auth_token)

        mensagem = f"Alerta de Preço para {alerta['produto']}: Preço Limite {alerta['preco_limite']}"
        
        try:
            message = client.messages.create(
                from_="+",
                body=mensagem,
                to=alerta["+"]
            )
            print(f"SMS enviado com sucesso. SID: {message.sid}")
        except Exception as e:
            print(f"Erro ao enviar SMS: {e}")
