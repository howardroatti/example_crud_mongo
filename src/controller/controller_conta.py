from model.contas import Conta
from model.clientes import Cliente
from conexion.oracle_queries import OracleQueries

class Controller_Conta:
    def __init__(self):
        pass
        
    def inserir_conta(self) -> Conta:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CNPJ
        nconta = input("N. Conta (Nova): ")

        if self.verifica_existencia_conta(oracle, nconta):
            # Solicita ao usuario o tipo da conta
            tipo = input("Tipo Conta (corrente, poupanca, credito) (Nova): ")
            # Solicita ao usuario o saldo da nova conta
            saldo = input("Saldo Inicial (Nova): ")
            # Solicita ao usuario o saldo da nova conta
            limite = input("Limite de Crédito (Nova): ")
            
            # Recupera dos clientes criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select id,nome,cpf,endereco,telefone from clientes")

            for i in range(df_cliente.index.size):
                # Cria um novo objeto Cliente
                ncliente = Cliente(df_cliente.id.values[i], df_cliente.cpf.values[i], df_cliente.nome.values[i], df_cliente.endereco.values[i], df_cliente.telefone.values[i])
                # Exibe os atributos do novo cliente
                print(ncliente.to_string())

            ncpf = input('Favor, informar CPF para a nova conta: ')

            dfclientid = oracle.sqlToDataFrame(f"select id from clientes where cpf = '{ncpf}'")
            codcli = dfclientid.id.values[0]
            
            # Insere e persiste o novo conta
            oracle.write(f"insert into contas values (seq_contas_id.nextval, '{nconta}', '{tipo}', '{saldo}', '{limite}', {codcli})")
            # Recupera os dados do novo conta criado transformando em um DataFrame
            df_conta = oracle.sqlToDataFrame(f"select id,numero,tipo,saldo, limite from contas where numero = '{nconta}'")
            # Cria um novo objeto conta
            nova_conta = Conta(df_conta.id.values[0], df_conta.numero.values[0], df_conta.tipo.values[0], df_conta.saldo.values[0], df_conta.limite.values[0])
            # Exibe os atributos do novo conta
            print(nova_conta.to_string())
            # Retorna o objeto novo_conta para utilização posterior, caso necessário
            return nova_conta
        else:
            print(f"A Conta {nconta} já está cadastrada.")
            return None

    def atualizar_conta(self) -> Conta:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do conta a ser alterado
        nconta = input("Número da conta que deseja atualizar: ")

        # Verifica se o conta existe na base de dados
        if not self.verifica_existencia_conta(oracle, nconta):
            # Solicita ao usuario o novo tipo da Conta
            ntipo = input("Tipo Conta (corrente, poupanca, credito): ")
            # Solicita ao usuario a nova razão social
            nlimite = input("Novo Limite: ")
           
            # Atualiza o nome do conta existente
            oracle.write(f"update contas set tipo = '{ntipo}', limite = '{nlimite}'  where numero = {nconta}")
            # Recupera os dados do novo conta criado transformando em um DataFrame
            df_conta = oracle.sqlToDataFrame(f"select numero,tipo,saldo, limite from contas where numero = '{nconta}'")
            # Cria um novo objeto conta
            conta_atualizado = Conta(df_conta.numero.values[0], df_conta.tipo.values[0], df_conta.saldo.values[0], df_conta.limite.values[0])
            # Exibe os atributos do novo conta
            print(conta_atualizado.to_string())
            # Retorna o objeto conta_atualizado para utilização posterior, caso necessário
            return conta_atualizado
        else:
            print(f"A conta {nconta} não existe.")
            return None

    def excluir_conta(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do conta a ser alterado
        nconta = input("Informar Número do conta que irá excluir: ")      

        # Verifica se o conta existe na base de dados
        if not self.verifica_existencia_conta(oracle, nconta):            
            # Recupera os dados do novo conta criado transformando em um DataFrame
            df_conta = oracle.sqlToDataFrame(f"select numero,tipo,saldo, limite from contas where numero = '{nconta}'")
            # Revome o conta da tabela
            oracle.write(f"delete from contas where numero = {nconta}")            
            # Cria um novo objeto conta para informar que foi removido
            conta_excluido = Conta(df_conta.numero.values[0], df_conta.tipo.values[0], df_conta.saldo.values[0], df_conta.limite.values[0])
            # Exibe os atributos do conta excluído
            print("conta Removido com Sucesso!")
            print(conta_excluido.to_string())
        else:
            print(f"A Conta {nconta} não existe.")

    def verifica_existencia_conta(self, oracle:OracleQueries, nconta:str=None) -> bool:
        # Recupera os dados do novo conta criado transformando em um DataFrame
        df_conta = oracle.sqlToDataFrame(f"select 1 from contas where numero = '{nconta}'")
        return df_conta.empty