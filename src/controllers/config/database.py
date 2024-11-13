from pymongo import MongoClient

class Database:
    _instance = None

    @staticmethod
    def get_instance():
        """Método para obter a instância Singleton do banco de dados."""
        if Database._instance is None:
            client = MongoClient("mongodb://localhost:27017/")
            Database._instance = client["alertas_db"]
        return Database._instance



# from pymongo import MongoClient

# def get_database():
#     client = MongoClient("mongodb://localhost:27017/")
#     return client["alertas_db"]

