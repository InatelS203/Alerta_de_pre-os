from twilio.rest import Client
import os

class TwilioClient:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def enviar_sms(self, to_number, mensagem):
        try:
            message = self.client.messages.create(
                from_=self.from_number,
                body=mensagem,
                to=to_number
            )
            return message.sid
        except Exception as e:
            print(f"Erro ao enviar SMS: {e}")
            return None
