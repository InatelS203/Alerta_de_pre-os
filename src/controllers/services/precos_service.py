# import pymongo
# import random
# from datetime import datetime

# # Conectar ao MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["sistema_precos"]
# collection = db["precos"]


# # Função para simular a obtenção de um novo preço
# def obter_novo_preco(preco_atual):
#     variacao = random.uniform(-0.1, 0.1)  # Simular flutuação de até 10%
#     return round(preco_atual * (1 + variacao), 2)


# # Função para atualizar o preço de um item no MongoDB
# def atualizar_preco(item_id, nome_item):
#     item = collection.find_one({"item_id": item_id})

#     if item:
#         preco_atual = item["preco_atual"]
#         novo_preco = obter_novo_preco(preco_atual)

#         # Atualizar o documento no MongoDB
#         collection.update_one(
#             {"item_id": item_id},
#             {
#                 "$set": {
#                     "preco_atual": novo_preco,
#                     "data_atualizacao": datetime.now().isoformat(),
#                 },
#                 "$push": {
#                     "historico_precos": {
#                         "preco": novo_preco,
#                         "data": datetime.now().isoformat(),
#                     }
#                 },
#             },
#         )
#         print(f"Preço do item '{nome_item}' atualizado para: {novo_preco}")
#     else:
#         print(f"Item '{nome_item}' não encontrado no banco de dados.")


# # Função para inserir um novo item no MongoDB (caso não exista)
# def inserir_item(item_id, nome_item, preco_inicial):
#     item_existente = collection.find_one({"item_id": item_id})
#     if not item_existente:
#         novo_item = {
#             "item_id": item_id,
#             "nome": nome_item,
#             "preco_atual": preco_inicial,
#             "preco_limite": preco_inicial - 1,  # Define o limite como preço inicial - 1
#             "status": "ativo",  # Marca o item como ativo
#             "historico_precos": [
#                 {"preco": preco_inicial, "data": datetime.now().isoformat()}
#             ],
#             "data_atualizacao": datetime.now().isoformat(),
#         }
#         collection.insert_one(novo_item)
#         print(f"Item '{nome_item}' inserido com preço inicial de: {preco_inicial}")
#     else:
#         print(f"Item '{nome_item}' já existe no banco de dados.")


# # Exemplo: Inserir alguns itens de cantina no banco de dados
# inserir_item("001", "coxinha", 6.0)
# inserir_item("002", "Refrigerante Lata", 3.5)
# inserir_item("003", "Sanduíche Natural", 8.0)

# # Simular atualizações de preço
# atualizar_preco("001", "coxinha")
# atualizar_preco("002", "Refrigerante Lata")
# atualizar_preco("003", "Sanduíche Natural")


import pymongo
import random
import schedule
import time
from datetime import datetime

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sistema_precos"]
collection = db["precos"]


# Função para simular a obtenção de um novo preço
def obter_novo_preco(preco_atual):
    variacao = random.uniform(-0.1, 0.1)  # Simular flutuação de até 10%
    novo_preco = round(preco_atual * (1 + variacao), 2)
    return novo_preco


# Função para atualizar o preço de um item no MongoDB
def atualizar_preco(item_id, nome_item):
    item = collection.find_one({"item_id": item_id})

    if item:
        preco_atual = item["preco_atual"]
        novo_preco = obter_novo_preco(preco_atual)

        # Atualizar o documento no MongoDB
        collection.update_one(
            {"item_id": item_id},
            {
                "$set": {
                    "preco_atual": novo_preco,
                    "data_atualizacao": datetime.now().isoformat(),
                },
                "$push": {
                    "historico_precos": {
                        "preco": novo_preco,
                        "data": datetime.now().isoformat(),
                    }
                },
            },
        )
        print(f"Preço do item '{nome_item}' atualizado para: {novo_preco}")
    else:
        print(f"Item '{nome_item}' não encontrado no banco de dados.")


# Função para inserir um novo item no MongoDB (caso não exista)
def inserir_item(item_id, nome_item, preco_inicial):
    item_existente = collection.find_one({"item_id": item_id})
    if not item_existente:
        novo_item = {
            "item_id": item_id,
            "nome": nome_item,
            "preco_atual": preco_inicial,
            "historico_precos": [
                {"preco": preco_inicial, "data": datetime.now().isoformat()}
            ],
            "data_atualizacao": datetime.now().isoformat(),
        }
        collection.insert_one(novo_item)
        print(f"Item '{nome_item}' inserido com preço inicial de: {preco_inicial}")
    else:
        print(f"Item '{nome_item}' já existe no banco de dados.")


# Função que atualiza todos os preços periodicamente
def simular_atualizacao_precos():
    items = collection.find()
    for item in items:
        atualizar_preco(item["item_id"], item["nome"])


# Exemplo: Inserir alguns itens de cantina no banco de dados
inserir_item("001", "Coxinha", 5.0)
inserir_item("002", "Refrigerante Lata", 3.5)
inserir_item("003", "Sanduíche Natural", 8.0)
inserir_item("004", "Pão de Queijo", 4.0)
inserir_item("005", "Suco Natural", 6.5)

# Agendar a atualização dos preços a cada 60 segundos
schedule.every(10).seconds.do(simular_atualizacao_precos)

# Loop para rodar o agendamento
while True:
    schedule.run_pending()
    time.sleep(1)
