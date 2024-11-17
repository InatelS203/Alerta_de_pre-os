from pymongo import MongoClient
from src.controllers.strategies.notification_factory import NotificationFactory


class NotificacaoService:
    def __init__(self):
        """
        Inicializa o serviço de notificações, conectando ao MongoDB.
        """
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["sistema_precos"]
        self.collection = self.db["precos"]
        self.notification_strategy = NotificationFactory.create_strategy("sms")

    def verificar_e_enviar_alertas(self):
        """
        Verifica os alertas com base nos dados do banco de dados e envia notificações quando necessário.
        """
        produtos = self.collection.find()

        for produto in produtos:
            preco_atual = produto.get("preco_atual", 0)
            preco_limite = produto.get("preco_limite", None)

            if preco_limite and preco_atual <= preco_limite:
                alerta = {
                    "produto": produto["nome"],
                    "preco_limite": preco_limite,
                    "preco_atual": preco_atual,
                    "telefone": produto.get("telefone", "+")
                }
                self.notification_strategy.send_notification(alerta)

    def monitorar_alteracoes(self):
        """
        Monitora alterações no banco de dados usando Change Streams do MongoDB.
        """
        try:
            with self.collection.watch() as stream:
                print("Monitorando alterações na coleção 'precos'...")
                for change in stream:
                    if change["operationType"] in ["update", "replace"]:
                        documento_id = change["documentKey"]["_id"]
                        produto = self.collection.find_one({"_id": documento_id})

                        if produto and produto["preco_atual"] <= produto["preco_limite"]:
                            alerta = {
                                "produto": produto["nome"],
                                "preco_limite": produto["preco_limite"],
                                "preco_atual": produto["preco_atual"],
                                "telefone": produto.get("telefone", "+")
                            }
                            self.notification_strategy.send_notification(alerta)
        except Exception as e:
            print(f"Erro ao monitorar alterações: {e}")


# Exemplo de execução direta
if __name__ == "__main__":
    notificacao_service = NotificacaoService()
    
    # Escolha uma das opções abaixo:
    
    # Executar monitoramento contínuo (requer suporte a Change Streams no MongoDB)
    notificacao_service.monitorar_alteracoes()
    
    # Executar verificação periódica (caso o Change Streams não esteja disponível)
    # notificacao_service.verificar_e_enviar_alertas()



# from src.controllers.strategies.notification_factory import NotificationFactory
# from src.controllers.repositories.alerta_repository import AlertaRepository

# class NotificacaoService:
#     def __init__(self, usar_simulacao=False):
#         """
#         Inicializa o serviço de notificações.
#         :param usar_simulacao: Indica se a busca de alertas será simulada ou feita no banco de dados.
#         """
#         self.usar_simulacao = usar_simulacao
#         self.repository = AlertaRepository()
#         self.notification_strategy = NotificationFactory.create_strategy("sms")

#     def verificar_e_enviar_alertas(self):
#         """
#         Verifica alertas ativos e envia notificações.
#         """
#         if self.usar_simulacao:
#             alertas = self.buscar_alertas_ativos_simulados()
#         else:
#             alertas = self.repository.buscar_alertas_ativos()

#         for alerta in alertas:
#             # Adiciona uma validação para garantir que todos os campos necessários estão presentes
#             if "preco_atual" not in alerta:
#                 alerta["preco_atual"] = "N/A"  # Valor padrão se preço atual não estiver presente

#             self.notification_strategy.send_notification(alerta)

#     @staticmethod
#     def buscar_alertas_ativos_simulados():
#         """
#         Retorna alertas simulados para fins de teste.
#         """
#         return [
#             {
#                 "produto": "Coxinha",
#                 "preco_limite": 4.0,
#                 "preco_atual": 3.5,  # Campo preco_atual adicionado
#                 "status": "ativo",
#                 "telefone": "+"
#             },
#             {
#                 "produto": "Refrigerante",
#                 "preco_limite": 5.0,
#                 "preco_atual": 5.2,  # Campo preco_atual adicionado
#                 "status": "ativo",
#                 "telefone": "+"
#             }
#         ]
# # Exemplo de execução direta
# if __name__ == "__main__":
#     notificacao_service = NotificacaoService(usar_simulacao=False)  # Troque para False para usar dados reais
#     notificacao_service.verificar_e_enviar_alertas()


# from src.controllers.repositories.alerta_repository import AlertaRepository
# from src.controllers.strategies.notification_factory import NotificationFactory

# class NotificacaoService:
#     def __init__(self, usar_simulacao=False):
#         """
#         Inicializa o serviço de notificações.
#         :param usar_simulacao: Indica se a busca de alertas será simulada ou real.
#         """
#         self.usar_simulacao = usar_simulacao
#         self.repository = AlertaRepository()
#         self.notification_strategy = NotificationFactory.create_strategy("sms")

#     def verificar_e_enviar_alertas(self):
#         """
#         Verifica os alertas ativos e envia notificações.
#         """
#         if self.usar_simulacao:
#             alertas = self.buscar_alertas_ativos_simulados()
#         else:
#             alertas = self.repository.buscar_alertas_ativos()

#         for alerta in alertas:
#             self.notification_strategy.send_notification(alerta)

#     @staticmethod
#     def buscar_alertas_ativos_simulados():
#         """
#         Função de exemplo para simular a busca de alertas ativos.
#         """
#         return [
#             {
#                 "produto": "Coxinha",
#                 "preco_limite": 4.0,
#                 "status": "ativo",
#                 "telefone": "+"  # Número de destino para SMS
#             },
#             {
#                 "produto": "Refrigerante",
#                 "preco_limite": 5.0,
#                 "status": "ativo",
#                 "telefone": "+"  # Número de destino para SMS
#             }
#         ]

# # Exemplo de execução direta
# if __name__ == "__main__":
#     notificacao_service = NotificacaoService(usar_simulacao=True)  # Troque para False para usar dados reais
#     notificacao_service.verificar_e_enviar_alertas()


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