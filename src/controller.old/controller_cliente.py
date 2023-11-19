import pandas as pd
from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries

class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_cliente(cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Insere e persiste o novo cliente
            self.mongo.db["clientes"].insert_one({"cpf": cpf, "nome": nome})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            self.mongo.close()
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = input("CPF do cliente que deseja alterar o nome: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpf):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do cliente existente
            self.mongo.db["clientes"].update_one({"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome}})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = input("CPF do Cliente que irá excluir: ")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(cpf):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Revome o cliente da tabela
            self.mongo.db["clientes"].delete_one({"cpf":f"{cpf}"})
            # Cria um novo objeto Cliente para informar que foi removido
            cliente_excluido = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0])
            self.mongo.close()
            # Exibe os atributos do cliente excluído
            print("Cliente Removido com Sucesso!")
            print(cliente_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_cliente(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(self.mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente.empty

    def recupera_cliente(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente