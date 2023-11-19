from utils.config import Recupera
import pandas as pd
from model.clientes import Cliente
from conexion.mongo_queries import MongoQueries
class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        self.recupera = Recupera()

    def inserir_cliente(self) -> Cliente:
                
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_cliente(cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")
            # Solicita Endereço
            endereco = input("Endereço: ")
            # Solicita Telefone
            telefone = input("telefone: ")

            # Insere e persiste o novo cliente
            #oracle.write(f"insert into clientes(id,nome,cpf,endereco,telefone) values (seq_clientes_id.nextval,'{nome}', '{cpf}', '{endereco}', '{telefone}')")
            
            novo_id = int(self.recupera.recupera_prox_id("clientes"))
            print(type(novo_id))

            self.mongo.db["clientes"].insert_one({"id": novo_id, "cpf": cpf, "nome": nome, "endereco": endereco, "telefone": telefone})
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.recupera_cliente(cpf)
            # Cria um novo objeto Cliente
            novo_cliente = Cliente(df_cliente.id.values[0], df_cliente.cpf.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0], df_cliente.telefone.values[0])
            # Exibe os atributos do novo cliente
            print(novo_cliente.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_cliente
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_cliente(self) -> Cliente:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = int(input("CPF do cliente que deseja alterar o nome: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do cliente existente
            oracle.write(f"update clientes set nome = '{novo_nome}' where cpf = {cpf}")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select id,nome,cpf,endereco,telefone from clientes where cpf = {cpf}")
            # Cria um novo objeto cliente
            cliente_atualizado = Cliente(df_cliente.id.values[0], df_cliente.cpf.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0], df_cliente.telefone.values[0])
            # Exibe os atributos do novo cliente
            print(cliente_atualizado.to_string())
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return cliente_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = int(input("CPF do Cliente que irá excluir: "))        

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):            
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select id,nome,cpf,endereco,telefone from clientes where cpf = {cpf}")
            # Revome o cliente da tabela
            oracle.write(f"delete from clientes where cpf = {cpf}")            
            # Cria um novo objeto Cliente para informar que foi removido
            cliente_excluido = Cliente(df_cliente.id.values[0], df_cliente.cpf.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0], df_cliente.telefone.values[0])
            # Exibe os atributos do cliente excluído
            print("Cliente Removido com Sucesso!")
            print(cliente_excluido.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_cliente(self,  cpf:str=None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um boolean
        df_cliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"cpf": 1})))
        return df_cliente.empty    
    
    def recupera_cliente(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"cpf":f"{cpf}"}, {"id":1 ,"cpf": 1, "nome": 1, "endereco": 1, "telefone": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente