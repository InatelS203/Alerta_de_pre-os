from src.controllers.strategies.notification_strategy import NotificationStrategy, SMSNotification
from twilio.rest import Client

class NotificationFactory:
    @staticmethod
    def create_strategy(strategy_type: str) -> NotificationStrategy:
        """
        Cria e retorna uma instância da estratégia de notificação especificada.
        :param strategy_type: Tipo de estratégia (ex.: "sms").
        :return: Instância de NotificationStrategy.
        """
        if strategy_type == "sms":
            # Configurar o cliente Twilio
            account_sid = ""
            auth_token = ""
            client = Client(account_sid, auth_token)
            return SMSNotification(client)
        else:
            raise ValueError(f"Estratégia de notificação desconhecida: {strategy_type}")
