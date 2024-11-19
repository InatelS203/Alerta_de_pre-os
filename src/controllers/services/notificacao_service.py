from src.controllers.strategies.notification_factory import NotificationFactory
from src.controllers.repositories.alerta_repository import AlertaRepository

class NotificacaoService:
    def __init__(self, usar_simulacao=False):
        """
        Inicializa o serviço de notificações.
        :param usar_simulacao: Indica se a busca de alertas será simulada ou feita no banco de dados.
        """
        self.usar_simulacao = usar_simulacao
        self.repository = AlertaRepository()
        self.notification_strategy = NotificationFactory.create_strategy("sms")
        self.ultimo_preco = {}  # Dicionário para rastrear o último preço notificado por produto

    def verificar_e_enviar_alertas(self):
        """
        Verifica alertas ativos e envia notificações apenas se o preço mudar.
        """
        print("Iniciando verificação de alertas...")
        if self.usar_simulacao:
            alertas = self.buscar_alertas_ativos_simulados()
        else:
            alertas = self.repository.buscar_alertas_ativos()

        for alerta in alertas:
            produto = alerta["produto"]
            preco_atual = alerta.get("preco_atual")
            preco_limite = alerta.get("preco_limite")

            # Validar campos obrigatórios
            if preco_atual is None or preco_limite is None:
                print(f"Alerta inválido: {alerta}")
                continue

            # Verificar se o preço mudou
            preco_anterior = self.ultimo_preco.get(produto)
            if preco_atual != preco_anterior:
                self.ultimo_preco[produto] = preco_atual
                # Enviar notificação somente se o preço atual for menor ou igual ao limite
                if preco_atual <= preco_limite:
                    self.notification_strategy.send_notification(alerta)
                    print(f"Mensagem enviada para {produto} com novo preço: {preco_atual}")
                else:
                    print(f"Preço de {produto} mudou para {preco_atual}, mas está acima do limite ({preco_limite}).")
            else:
                print(f"Preço de {produto} não mudou: {preco_atual}")

    @staticmethod
    def buscar_alertas_ativos_simulados():
        """
        Retorna alertas simulados para fins de teste.
        """
        return [
            {
                "produto": "Coxinha",
                "preco_limite": 4.0,
                "preco_atual": 3.5,
                "status": "ativo",
                "telefone": "+5533999678554"
            },
            {
                "produto": "Refrigerante",
                "preco_limite": 5.0,
                "preco_atual": 5.2,
                "status": "ativo",
                "telefone": "+5533999678554"
            }
        ]

# Exemplo de execução direta
if __name__ == "__main__":
    notificacao_service = NotificacaoService(usar_simulacao=False)  # Troque para True para usar dados simulados
    notificacao_service.verificar_e_enviar_alertas()


# from pymongo import MongoClient
# from src.controllers.strategies.notification_factory import NotificationFactory
# import time


# class NotificacaoService:
#     def __init__(self):
#         """
#         Inicializa o serviço de notificações.
#         """
#         self.client = MongoClient("mongodb://localhost:27017/")
#         self.db = self.client["sistema_precos"]
#         self.collection = self.db["alertas"]
#         self.collection_preco = self.db["precos"]
#         self.notification_strategy = NotificationFactory.create_strategy("sms")

#     def verificar_e_enviar_alertas(self):
#         """
#         Verifica os alertas ativos no banco de dados e envia notificações quando necessário.
#         """
#         print("Iniciando verificação de alertas...")

#         try:
#             # Buscar alertas ativos no banco de dados
#             alertas = self.buscar_alertas_ativos()

#             if not alertas:
#                 print("Nenhum alerta ativo encontrado no banco de dados.")
#                 return

#             for alerta in alertas:
#                 # Verificar se o preço atual está abaixo ou igual ao limite
#                 produto = list(self.collection_preco.find({"nome": alerta["nome"]}))
#                 print(produto[0]["preco_atual"])
#                 if (produto["preco_atual"] <= alerta.get("preco_limite", 0)) and alerta["flag"] == 0:
#                     self.notification_strategy.send_notification(alerta)
#                     print(f"Alerta enviado para o produto {alerta['nome']}!")
#                 elif alerta["flag"] == 1:
#                     print(f"Preço do produto '{alerta['nome']}' ainda acima do limite definido.")
#                 else:
#                     print(f"Preço do produto '{alerta['nome']}' ainda abaixo do limite definido.")

#         except Exception as e:
#             print(f"Erro ao verificar e enviar alertas: {e}")

#     def buscar_alertas_ativos(self):
#         """
#         Busca itens ativos no banco de dados que atendem às condições de notificação.
#         """
#         try:
#             # Busca por itens com status "ativo"
#             alertas = list(self.collection.find({"status": "ativo"}))
#             if not alertas:
#                 print("Nenhum alerta ativo foi encontrado no banco de dados.")
#             return alertas
#         except Exception as e:
#             print(f"Erro ao buscar alertas ativos: {e}")
#             return []

#     def iniciar_monitoramento(self):
#         """
#         Inicia o monitoramento contínuo dos alertas.
#         """
#         print("Monitoramento de alertas iniciado.")
#         while True:
#             self.verificar_e_enviar_alertas()
#             time.sleep(10)  # Intervalo de 60 segundos entre as verificações


# if __name__ == "__main__":
#     notificacao_service = NotificacaoService()
#     notificacao_service.iniciar_monitoramento()


