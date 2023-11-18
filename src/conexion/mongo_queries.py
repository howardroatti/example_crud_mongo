import pymongo

class MongoQueries:
    def __init__(self):
        self.host = "192.168.1.250"
        self.port = 27017
        self.service_name = 'mivie'

        with open("conexion/passphrase/authentication.mongo", "r") as f:
            self.user, self.passwd = f.read().split(',')

    def __del__(self):
        if hasattr(self, "mongo_client"):
            self.close()

    def connect(self):
        self.mongo_client = pymongo.MongoClient(f"mongodb://{self.user}:{self.passwd}@192.168.1.250:27017/")
        self.db = self.mongo_client["mivie"]

    def close(self):
        self.mongo_client.close()