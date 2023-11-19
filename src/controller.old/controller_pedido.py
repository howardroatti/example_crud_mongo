import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.pedidos import Pedido
from model.clientes import Cliente
from model.fornecedores import Fornecedor

from controller.controller_cliente import Controller_Cliente
from controller.controller_fornecedor import Controller_Fornecedor

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Pedido:
    def __init__(self):
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_fornecedor = Controller_Fornecedor()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_pedido(self) -> Pedido:
        # Cria uma nova conexão com o banco
        self.mongo.connect()
        
        # Lista os clientes existentes para inserir no pedido
        self.relatorio.get_relatorio_clientes()
        cpf = str(input("Digite o número do CPF do Cliente: "))
        cliente = self.valida_cliente(cpf)
        if cliente == None:
            return None

        # Lista os fornecedores existentes para inserir no pedido
        self.relatorio.get_relatorio_fornecedores()
        cnpj = str(input("Digite o número do CNPJ do Fornecedor: "))
        fornecedor = self.valida_fornecedor(cnpj)
        if fornecedor == None:
            return None

        data_hoje = datetime.today().strftime("%m-%d-%Y")
        proximo_pedido = self.mongo.db["pedidos"].aggregate([
                                                            {
                                                                '$group': {
                                                                    '_id': '$pedidos', 
                                                                    'proximo_pedido': {
                                                                        '$max': '$codigo_pedido'
                                                                    }
                                                                }
                                                            }, {
                                                                '$project': {
                                                                    'proximo_pedido': {
                                                                        '$sum': [
                                                                            '$proximo_pedido', 1
                                                                        ]
                                                                    }, 
                                                                    '_id': 0
                                                                }
                                                            }
                                                        ])

        proximo_pedido = int(list(proximo_pedido)[0]['proximo_pedido'])
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo_pedido=proximo_pedido, data_pedido=data_hoje, cpf=cliente.get_CPF(), cnpj=fornecedor.get_CNPJ())
        # Insere e Recupera o código do novo pedido
        id_pedido = self.mongo.db["pedidos"].insert_one(data)
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_pedido = self.recupera_pedido(id_pedido.inserted_id)
        # Cria um novo objeto Produto
        novo_pedido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
        # Exibe os atributos do novo produto
        print(novo_pedido.to_string())
        self.mongo.close()
        # Retorna o objeto novo_pedido para utilização posterior, caso necessário
        return novo_pedido

    def atualizar_pedido(self) -> Pedido:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_pedido = int(input("Código do Pedido que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_pedido(codigo_pedido):

            # Lista os clientes existentes para inserir no pedido
            self.relatorio.get_relatorio_clientes()
            cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(cpf)
            if cliente == None:
                return None

            # Lista os fornecedores existentes para inserir no pedido
            self.relatorio.get_relatorio_fornecedores()
            cnpj = str(input("Digite o número do CNPJ do Fornecedor: "))
            fornecedor = self.valida_fornecedor(cnpj)
            if fornecedor == None:
                return None

            data_hoje = datetime.today().strftime("%m-%d-%Y")

            # Atualiza a descrição do produto existente
            self.mongo.db["pedidos"].update_one({"codigo_pedido": codigo_pedido}, 
                                                {"$set": {"cnpj": f'{fornecedor.get_CNPJ()}',
                                                          "cpf":  f'{cliente.get_CPF()}',
                                                          "data_pedido": data_hoje
                                                          }
                                                })
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_pedido = self.recupera_pedido_codigo(codigo_pedido)
            # Cria um novo objeto Produto
            pedido_atualizado = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
            # Exibe os atributos do novo produto
            print(pedido_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return pedido_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_pedido} não existe.")
            return None

    def excluir_pedido(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_pedido = int(input("Código do Pedido que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_pedido(codigo_pedido):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_pedido = self.recupera_pedido_codigo(codigo_pedido)
            cliente = self.valida_cliente(df_pedido.cpf.values[0])
            fornecedor = self.valida_fornecedor(df_pedido.cnpj.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_pedido} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o pedido possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_pedido} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    self.mongo.db["itens_pedido"].delete_one({"codigo_pedido": codigo_pedido})
                    print("Itens do pedido removidos com sucesso!")
                    self.mongo.db["pedidos"].delete_one({"codigo_pedido": codigo_pedido})
                    # Cria um novo objeto Produto para informar que foi removido
                    pedido_excluido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
                    self.mongo.close()
                    # Exibe os atributos do produto excluído
                    print("Pedido Removido com Sucesso!")
                    print(pedido_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_pedido} não existe.")

    def verifica_existencia_pedido(self, codigo:int=None, external: bool = False) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = self.recupera_pedido_codigo(codigo=codigo, external=external)
        return df_pedido.empty

    def recupera_pedido(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = pd.DataFrame(list(self.mongo.db["pedidos"].find({"_id":_id}, {"codigo_pedido": 1, "data_pedido": 1, "cpf": 1, "cnpj": 1, "_id": 0})))
        return df_pedido

    def recupera_pedido_codigo(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = pd.DataFrame(list(self.mongo.db["pedidos"].find({"codigo_pedido": codigo}, {"codigo_pedido": 1, "data_pedido": 1, "cpf": 1, "cnpj": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_pedido

    def valida_cliente(self, cpf:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(cpf=cpf, external=True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.ctrl_cliente.recupera_cliente(cpf=cpf, external=True)
            # Cria um novo objeto cliente
            cliente = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
            return cliente

    def valida_fornecedor(self, cnpj:str=None) -> Fornecedor:
        if self.ctrl_fornecedor.verifica_existencia_fornecedor(cnpj, external=True):
            print(f"O CNPJ {cnpj} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_fornecedor = self.ctrl_fornecedor.recupera_fornecedor(cnpj, external=True)
            # Cria um novo objeto fornecedor
            fornecedor = Fornecedor(df_fornecedor.cnpj.values[0], df_fornecedor.razao_social.values[0], df_fornecedor.nome_fantasia.values[0])
            return fornecedor