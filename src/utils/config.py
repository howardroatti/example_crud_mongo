MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Pedidos por Fornecedores
2 - Relatório de Pedidos
3 - Relatório de Produtos
4 - Relatório de Clientes
5 - Relatório de Fornecedores
6 - Relatório de Itens de Pedidos
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - PRODUTOS
2 - CLIENTES
3 - FORNECEDORES
4 - PEDIDOS
5 - ITENS DE PEDIDOS
"""

# Consulta de contagem de registros por tabela
def query_count(collection_name):
   from conexion.mongo_queries import MongoQueries
   import pandas as pd

   mongo = MongoQueries()
   mongo.connect()

   my_collection = mongo.db[collection_name]
   total_documentos = my_collection.count_documents({})
   mongo.close()
   df = pd.DataFrame({f"total_{collection_name}": [total_documentos]})
   return df

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")