from src.controllers.strategies.notification_strategy import SMSNotification

class NotificationFactory:
    @staticmethod
    def create_notification(notification_type):
        if notification_type == 'sms':
            return SMSNotification()
        else:
            raise ValueError("Tipo de notificação desconhecido")
