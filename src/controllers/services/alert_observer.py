class AlertObserver:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def notify(self, alerta):
        for subscriber in self.subscribers:
            subscriber.update(alerta)

#Para gerenciar o envio de alertas em tempo real, o padrão Observer permite que as mudanças nos preços dos produtos notifiquem automaticamente os interessados (usuários ou serviços).