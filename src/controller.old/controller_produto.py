from bson import ObjectId
import pandas as pd
from model.produtos import Produto
from conexion.mongo_queries import MongoQueries

class Controller_Produto:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_produto(self) -> Produto:
        # Cria uma nova conexão com o banco
        self.mongo.connect()
        
        #Solicita ao usuario a nova descrição do produto
        descricao_novo_produto = input("Descrição (Novo): ")
        proximo_produto = self.mongo.db["produtos"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$produtos', 
                                                            'proximo_produto': {
                                                                '$max': '$codigo_produto'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_produto': {
                                                                '$sum': [
                                                                    '$proximo_produto', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_produto = int(list(proximo_produto)[0]['proximo_produto'])
        
        # Insere e Recupera o código do novo produto
        id_produto = self.mongo.db["produtos"].insert_one({"codigo_produto": proximo_produto, "descricao_produto": descricao_novo_produto})
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = self.recupera_produto(id_produto.inserted_id)
        # Cria um novo objeto Produto
        novo_produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
        # Exibe os atributos do novo produto
        print(novo_produto.to_string())
        self.mongo.close()
        # Retorna o objeto novo_produto para utilização posterior, caso necessário
        return novo_produto

    def atualizar_produto(self) -> Produto:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_produto = int(input("Código do Produto que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_produto(codigo_produto):
            # Solicita a nova descrição do produto
            nova_descricao_produto = input("Descrição (Novo): ")
            # Atualiza a descrição do produto existente
            self.mongo.db["produtos"].update_one({"codigo_produto": codigo_produto}, {"$set": {"descricao_produto": nova_descricao_produto}})
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_produto = self.recupera_produto_codigo(codigo_produto)
            # Cria um novo objeto Produto
            produto_atualizado = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            # Exibe os atributos do novo produto
            print(produto_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto produto_atualizado para utilização posterior, caso necessário
            return produto_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_produto} não existe.")
            return None

    def excluir_produto(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_produto = int(input("Código do Produto que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_produto(codigo_produto):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_produto = self.recupera_produto_codigo(codigo_produto)
            # Revome o produto da tabela
            self.mongo.db["produtos"].delete_one({"codigo_produto": codigo_produto})
            # Cria um novo objeto Produto para informar que foi removido
            produto_excluido = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            # Exibe os atributos do produto excluído
            print("Produto Removido com Sucesso!")
            print(produto_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O código {codigo_produto} não existe.")

    def verifica_existencia_produto(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = pd.DataFrame(self.mongo.db["produtos"].find({"codigo_produto":codigo}, {"codigo_produto": 1, "descricao_produto": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_produto.empty

    def recupera_produto(self, _id:ObjectId=None) -> pd.DataFrame:
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = pd.DataFrame(list(self.mongo.db["produtos"].find({"_id":_id}, {"codigo_produto": 1, "descricao_produto": 1, "_id": 0})))
        return df_produto

    def recupera_produto_codigo(self, codigo:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = pd.DataFrame(list(self.mongo.db["produtos"].find({"codigo_produto":codigo}, {"codigo_produto": 1, "descricao_produto": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_produto