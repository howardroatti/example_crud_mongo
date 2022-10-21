import pandas as pd
from model.fornecedores import Fornecedor
from conexion.mongo_queries import MongoQueries

class Controller_Fornecedor:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_fornecedor(self) -> Fornecedor:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo CNPJ
        cnpj = input("CNPJ (Novo): ")

        if self.verifica_existencia_fornecedor(cnpj):
            # Solicita ao usuario a nova razão social
            razao_social = input("Razão Social (Novo): ")
            # Solicita ao usuario o novo nome fantasia
            nome_fantasia = input("Nome Fantasia (Novo): ")
            # Insere e persiste o novo fornecedor
            self.mongo.db["fornecedores"].insert_one({"cnpj": cnpj, "razao_social": razao_social, "nome_fantasia": nome_fantasia})
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_fornecedor = self.recupera_fornecedor(cnpj)
            # Cria um novo objeto fornecedor
            novo_fornecedor = Fornecedor(df_fornecedor.cnpj.values[0], df_fornecedor.razao_social.values[0], df_fornecedor.nome_fantasia.values[0])
            # Exibe os atributos do novo fornecedor
            print(novo_fornecedor.to_string())
            self.mongo.close()
            # Retorna o objeto novo_fornecedor para utilização posterior, caso necessário
            return novo_fornecedor
        else:
            self.mongo.close()
            print(f"O CNPJ {cnpj} já está cadastrado.")
            return None

    def atualizar_fornecedor(self) -> Fornecedor:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do fornecedor a ser alterado
        cnpj = int(input("CNPJ do fornecedor que deseja atualizar: "))

        # Verifica se o fornecedor existe na base de dados
        if not self.verifica_existencia_fornecedor(cnpj):
            # Solicita ao usuario a nova razão social
            razao_social = input("Razão Social (Novo): ")
            # Solicita ao usuario o novo nome fantasia
            nome_fantasia = input("Nome Fantasia (Novo): ")            
            # Atualiza o nome do fornecedor existente
            self.mongo.db["fornecedores"].update_one({"cnpj":f"{cnpj}"},{"$set": {"razao_social":razao_social, "nome_fantasia":nome_fantasia}})
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_fornecedor = self.recupera_fornecedor(cnpj)
            # Cria um novo objeto fornecedor
            fornecedor_atualizado = Fornecedor(df_fornecedor.cnpj.values[0], df_fornecedor.razao_social.values[0], df_fornecedor.nome_fantasia.values[0])
            # Exibe os atributos do novo fornecedor
            print(fornecedor_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto fornecedor_atualizado para utilização posterior, caso necessário
            return fornecedor_atualizado
        else:
            self.mongo.close()
            print(f"O CNPJ {cnpj} não existe.")
            return None

    def excluir_fornecedor(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o CPF do fornecedor a ser alterado
        cnpj = int(input("CNPJ do fornecedor que irá excluir: "))        

        # Verifica se o fornecedor existe na base de dados
        if not self.verifica_existencia_fornecedor(cnpj):            
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_fornecedor = self.recupera_fornecedor(cnpj)
            # Revome o fornecedor da tabela
            self.mongo.db["fornecedores"].delete_one({"cnpj":f"{cnpj}"})
            # Cria um novo objeto fornecedor para informar que foi removido
            fornecedor_excluido = Fornecedor(df_fornecedor.cnpj.values[0], df_fornecedor.razao_social.values[0], df_fornecedor.nome_fantasia.values[0])
            self.mongo.close()
            # Exibe os atributos do fornecedor excluído
            print("fornecedor Removido com Sucesso!")
            print(fornecedor_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O CNPJ {cnpj} não existe.")

    def verifica_existencia_fornecedor(self, cnpj:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo fornecedor criado transformando em um DataFrame
        df_fornecedor = pd.DataFrame(self.mongo.db["fornecedores"].find({"cnpj":f"{cnpj}"}, {"cnpj": 1, "razao_social": 1, "nome_fantasia": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_fornecedor.empty

    def recupera_fornecedor(self, cnpj:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["fornecedores"].find({"cnpj":f"{cnpj}"}, {"cnpj": 1, "razao_social": 1, "nome_fantasia": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente