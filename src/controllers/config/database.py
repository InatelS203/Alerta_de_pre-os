from pymongo import MongoClient

class Database:
    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database._instance = MongoClient("mongodb://localhost:27017/")["alertas_db"]
        return Database._instance

def get_database():
    return Database.get_instance()


# from pymongo import MongoClient

# def get_database():
#     client = MongoClient("mongodb://localhost:27017/")
#     return client["alertas_db"]

