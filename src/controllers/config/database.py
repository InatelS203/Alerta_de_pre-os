from pymongo import MongoClient

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = MongoClient("mongodb://localhost:27017/")
            cls._instance.db = cls._instance.client["alertas_db"]
        return cls._instance

    def get_collection(self, collection_name):
        return self._instance.db[collection_name]



# from pymongo import MongoClient

# def get_database():
#     client = MongoClient("mongodb://localhost:27017/")
#     return client["alertas_db"]

