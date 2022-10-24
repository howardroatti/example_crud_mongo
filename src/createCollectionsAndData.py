import logging
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries
import json

LIST_OF_COLLECTIONS = ["fornecedores", "clientes", "produtos", "pedidos", "itens_pedido"]
logger = logging.getLogger(name="Example_CRUD_MongoDB")
logger.setLevel(level=logging.WARNING)
mongo = MongoQueries()

def createCollections(drop_if_exists:bool=False):
    """
        Lista as coleções existentes, verificar se as coleções padrão estão entre as coleções existentes.
        Caso exista e o parâmetro de exclusão esteja configurado como True, irá apagar a coleção e criar novamente.
        Caso não exista, cria a coleção.
        
        Parameter:
                  - drop_if_exists: True  -> apaga a tabela existente e recria
                                    False -> não faz nada
    """
    mongo.connect()
    existing_collections = mongo.db.list_collection_names()
    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} droped!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} created!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")
    mongo.close()

def insert_many(data:json, collection:str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()

def extract_and_insert():
    oracle = OracleQueries()
    oracle.connect()
    sql = "select * from labdatabase.{table}"
    for collection in LIST_OF_COLLECTIONS:
        df = oracle.sqlToDataFrame(sql.format(table=collection))
        if collection == "pedidos":
            df["data_pedido"] = df["data_pedido"].dt.strftime("%m-%d-%Y")
        logger.warning(f"data extracted from database Oracle labdatabase.{collection}")
        records = json.loads(df.T.to_json()).values()
        logger.warning("data converted to json")
        insert_many(data=records, collection=collection)
        logger.warning(f"documents generated at {collection} collection")

if __name__ == "__main__":
    logging.warning("Starting")
    createCollections(drop_if_exists=True)
    extract_and_insert()
    logging.warning("End")
