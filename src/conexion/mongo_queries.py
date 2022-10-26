import pymongo

class MongoQueries:
    def __init__(self):
        self.host = "localhost"
        self.port = 27017
        self.service_name = 'labdatabase'

        with open("conexion/passphrase/authentication.mongo", "r") as f:
            self.user, self.passwd = f.read().split(',')

    def __del__(self):
        if hasattr(self, "mongo_client"):
            self.close()

    def connect(self):
        self.mongo_client = pymongo.MongoClient(f"mongodb://{self.user}:{self.passwd}@localhost:27017/")
        self.db = self.mongo_client["labdatabase"]

    def close(self):
        self.mongo_client.close()