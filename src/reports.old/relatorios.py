from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_pedidos_e_itens(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db.pedidos.aggregate([{
                                                    "$lookup":{"from":"itens_pedido",
                                                               "localField":"codigo_pedido",
                                                               "foreignField":"codigo_pedido",
                                                               "as":"item"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": { "path": "$item"}
                                                   },
                                                   {
                                                    "$lookup":{"from":"clientes",
                                                               "localField":"cpf",
                                                               "foreignField":"cpf",
                                                               "as":"cliente"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": { "path": "$cliente" }
                                                   },
                                                   {
                                                    "$lookup":{"from":"fornecedores",
                                                               "localField":"cnpj",
                                                               "foreignField":"cnpj",
                                                               "as":"fornecedor"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": {"path": "$fornecedor"}
                                                   },
                                                   {
                                                    "$lookup":{"from":'produtos',
                                                               "localField":"item.codigo_produto",
                                                               "foreignField":"codigo_produto",
                                                               "as":"produto"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": {"path": "$produto"}
                                                   },
                                                   {
                                                    "$project": {"codigo_pedido": 1,
                                                                 "codigo_item_pedido": "$item.codigo_item_pedido",
                                                                 "cliente": "$cliente.nome",
                                                                 "data_pedido":1,
                                                                 "fornecedor": "$fornecedor.razao_social",
                                                                 "produto": "$produto.descricao_produto",
                                                                 "quantidade": "$item.quantidade",
                                                                 "valor_unitario": "$item.valor_unitario",
                                                                 "valor_total": {'$multiply':['$item.quantidade','$item.valor_unitario']},
                                                                 "_id": 0
                                                                }
                                                   }])
        
        df_pedidos_itens = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_pedidos_itens)
        input("Pressione Enter para Sair do Relatório de Pedidos")

    def get_relatorio_pedidos_por_fornecedor(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pedidos"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$cnpj', 
                                                            'qtd_pedidos': {
                                                                '$sum': 1
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': '$_id', 
                                                            'qtd_pedidos': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'pedidos', 
                                                            'localField': 'cnpj', 
                                                            'foreignField': 'cnpj', 
                                                            'as': 'pedido'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$pedido'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': 1, 
                                                            'qtd_pedidos': 1, 
                                                            'pedido': '$pedido.codigo_pedido', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'itens_pedido', 
                                                            'localField': 'pedido', 
                                                            'foreignField': 'codigo_pedido', 
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': 1, 
                                                            'qtd_pedidos': 1, 
                                                            'quantidade': '$item.quantidade', 
                                                            'valor_unitario': '$item.valor_unitario', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$group': {
                                                            '_id': {
                                                                'cnpj': '$cnpj', 
                                                                'qtd_pedidos': '$qtd_pedidos'
                                                            }, 
                                                            'valor_total': {
                                                                '$sum': {
                                                                    '$multiply': [
                                                                        '$quantidade', '$valor_unitario'
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$_id'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'cnpj': '$_id.cnpj', 
                                                            'qtd_pedidos': '$_id.qtd_pedidos', 
                                                            'valor_total': '$valor_total', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'fornecedores', 
                                                            'localField': 'cnpj', 
                                                            'foreignField': 'cnpj', 
                                                            'as': 'fornecedor'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$fornecedor'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'empresa': '$fornecedor.nome_fantasia', 
                                                            'qtd_pedidos': 1, 
                                                            'valor_total': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'empresa': 1
                                                        }
                                                    }
                                                ])
        df_pedidos_fornecedor = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_pedidos_fornecedor[["empresa", "qtd_pedidos", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Fornecedores")

    def get_relatorio_produtos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["produtos"].find({}, 
                                                 {"codigo_produto": 1, 
                                                  "descricao_produto": 1, 
                                                  "_id": 0
                                                 }).sort("descricao_produto", ASCENDING)
        df_produto = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        # Exibe o resultado
        print(df_produto)        
        input("Pressione Enter para Sair do Relatório de Produtos")

    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["clientes"].find({}, 
                                                 {"cpf": 1, 
                                                  "nome": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_cliente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_cliente)
        input("Pressione Enter para Sair do Relatório de Clientes")

    def get_relatorio_fornecedores(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["fornecedores"].find({}, 
                                                     {"cnpj": 1, 
                                                      "razao_social": 1, 
                                                      "nome_fantasia": 1, 
                                                      "_id": 0
                                                     }).sort("nome_fantasia", ASCENDING)
        df_fornecedor = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_fornecedor)        
        input("Pressione Enter para Sair do Relatório de Fornecedores")

    def get_relatorio_pedidos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pedidos"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'fornecedores', 
                                                            'localField': 'cnpj', 
                                                            'foreignField': 'cnpj', 
                                                            'as': 'fornecedor'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$fornecedor'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': '$fornecedor.nome_fantasia', 
                                                            'cpf': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'clientes', 
                                                            'localField': 'cpf', 
                                                            'foreignField': 'cpf', 
                                                            'as': 'cliente'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$cliente'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': 1, 
                                                            'cliente': '$cliente.nome', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'itens_pedido', 
                                                            'localField': 'codigo_pedido', 
                                                            'foreignField': 'codigo_pedido', 
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': 1, 
                                                            'cliente': 1, 
                                                            'item_pedido': '$item.codigo_item_pedido', 
                                                            'quantidade': '$item.quantidade', 
                                                            'valor_unitario': '$item.valor_unitario', 
                                                            'valor_total': {
                                                                '$multiply': [
                                                                    '$item.quantidade', '$item.valor_unitario'
                                                                ]
                                                            }, 
                                                            'codigo_produto': '$item.codigo_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'produtos', 
                                                            'localField': 'codigo_produto', 
                                                            'foreignField': 'codigo_produto', 
                                                            'as': 'produto'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$produto', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': 1, 
                                                            'cliente': 1, 
                                                            'item_pedido': 1, 
                                                            'quantidade': 1, 
                                                            'valor_unitario': 1, 
                                                            'valor_total': 1, 
                                                            'produto': '$produto.descricao_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'cliente': 1,
                                                            'item_pedido': 1
                                                        }
                                                    }
                                                ])
        df_pedido = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_pedido[["codigo_pedido", "data_pedido", "cliente", "empresa", "item_pedido", "produto", "quantidade", "valor_unitario", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Pedidos")
    
    def get_relatorio_itens_pedidos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db['itens_pedido'].aggregate([{
                                                            '$lookup':{'from':'produtos',
                                                                       'localField':'codigo_produto',
                                                                       'foreignField':'codigo_produto',
                                                                       'as':'produto'
                                                                      }
                                                           },
                                                           {
                                                            '$unwind':{"path": "$produto"}
                                                           },
                                                           {'$project':{'codigo_pedido':1, 
                                                                        'codigo_item_pedido':1,
                                                                    'codigo_produto':'$produto.codigo_produto',
                                                                    'descricao_produto':'$produto.descricao_produto',
                                                                    'quantidade':1,
                                                                    'valor_unitario':1,
                                                                    'valor_total':{'$multiply':['$quantidade','$valor_unitario']},
                                                                    '_id':0
                                                                    }}
                                                          ])
        # Converte o cursos em lista e em DataFrame
        df_itens_pedido = pd.DataFrame(list(query_result))
        # Troca o tipo das colunas
        df_itens_pedido.codigo_item_pedido = df_itens_pedido.codigo_item_pedido.astype(int)
        df_itens_pedido.codigo_pedido = df_itens_pedido.codigo_pedido.astype(int)
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_itens_pedido[["codigo_pedido", "codigo_item_pedido", "codigo_produto", "descricao_produto", "quantidade", "valor_unitario", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Itens de Pedidos")