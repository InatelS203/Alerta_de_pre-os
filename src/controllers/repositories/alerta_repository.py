from pymongo import MongoClient


class AlertaRepository:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["sistema_precos"]
        self.alertas_collection = self.db["alertas"]
        self.precos_collection = self.db["precos"]

    def buscar_alertas_ativos(self):
        """
        Retorna alertas ativos no banco de dados.
        """
        return list(self.alertas_collection.find({"status": "ativo"}))

    def buscar_preco_produto(self, produto):
        """
        Retorna o preço atual de um produto específico.
        """
        return self.precos_collection.find_one({"nome": produto})



# from pymongo import MongoClient

# class AlertaRepository:
#     def __init__(self):
#         self.client = MongoClient("mongodb://localhost:27017/")
#         self.db = self.client['sistema_precos']  # Certifique-se de usar o mesmo nome de banco usado no preco_service
#         self.collection = self.db['precos']

#     def buscar_alertas_ativos(self):
#         """
#         Busca alertas ativos no banco de dados.
#         Um alerta é considerado ativo se o status for 'ativo' e ele contiver os campos necessários.
#         """
#         try:
#             # Filtra alertas com status 'ativo'
#             alertas = self.collection.find({"status": "ativo"})
#             return [
#                 {
#                     "produto": alerta["nome"],
#                     "preco_atual": alerta["preco_atual"],
#                     "preco_limite": alerta.get("preco_limite", None),  # Preço limite pode ser opcional
#                     "telefone": alerta.get("telefone", None),
#                 }
#                 for alerta in alertas
#                 if "preco_atual" in alerta and "nome" in alerta
#             ]
#         except Exception as e:
#             print(f"Erro ao buscar alertas no banco de dados: {e}")
#             return []


# from src.controllers.config.database import get_database

# class AlertaRepository:
#     def __init__(self):
#         self.collection = get_database()["alertas"]

#     def buscar_alertas_ativos(self):
#         """
#         Busca alertas ativos no banco de dados.
#         """
#         return list(self.collection.find({"status": "ativo"}))
