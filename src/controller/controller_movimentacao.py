from model.movimentacoes import Movimentacao
from model.contas import Conta
from controller.controller_conta import Controller_Conta
from conexion.oracle_queries import OracleQueries
import datetime

class Controller_Movimentacao:
    def __init__(self):
        self.ctrl_conta = Controller_Conta()
        
    def inserir_movimentacao(self) -> Movimentacao:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista os pedido existentes para inserir no item de pedido
        self.listar_contas(oracle, need_connect=True)
        lnumero = int(input("Digite o número da Conta: "))
        nconta = self.valida_conta(oracle, lnumero)
        if nconta == None:
            return None

        '''datamov = datetime.datetime.now()
        x = datamov.strftime("%d/%m/%Y %H:%M:%S")
        print(x) '''

        tipomov = input("Informar o Tipo da Movimemtação (C)rédito ou (D)ébito: ")

        vvalor = float(input("Informar o Valor da Movimentação: "))

        if (vvalor.__lt__(0)):
            print("Valor inválido - não pode ser negativo")
            return None

        vcontaid = nconta.get_id()
        vcontasaldo = nconta.get_saldo()
        vcontalimite = nconta.get_limite()
        vnumeroconta = nconta.get_numero()
        vsaldoatu = 0

        if tipomov.upper() == 'C':
            vdesc = 'CREDITO EM CONTA'
            vsaldoant = vcontasaldo
            vsaldoatu = vcontasaldo + vvalor
        elif tipomov.upper() == 'D':
            vdesc = 'DÉBITO EM CONTA'
            vsaldoant = vcontasaldo
            vsaldoatu = vcontasaldo - vvalor
            vvalor = vvalor*-1
        else:
            print("Favor, informar (C)rédito ou (D)ébito.")
            return None

        if (vcontalimite*-1) <= vsaldoatu:
            # Cria uma nova conexão com o banco que permite alteração
            oracle = OracleQueries(can_write=True)
            oracle.connect()
            # Insere e persiste o novo saldo e movimento
            df_idmov = oracle.sqlToDataFrame(f"select seq_movimentacoes_id.nextval as id from dual")
            # Cria um novo objeto conta
            idmov = df_idmov.id.values[0]
            oracle.write(f"update contas set saldo = {vsaldoatu} where id = {vcontaid}",False)
            oracle.write(f"insert into movimentacoes values ({idmov}, sysdate, '{vdesc}', '{vvalor}', '{vsaldoant}', '{vsaldoatu}', '{vcontaid}')")
            # Recupera os dados do novo conta criado transformando em um DataFrame
            df_mov = oracle.sqlToDataFrame(f"select '{vnumeroconta}' as num,id, data, descricao, valor, saldo_anterior, saldo_atual from movimentacoes where id = {idmov}")
            # Cria um novo objeto conta
            nova_mov = Movimentacao(df_mov.id.values[0], df_mov.data.values[0], df_mov.descricao.values[0], df_mov.valor.values[0], df_mov.saldo_anterior.values[0],df_mov.saldo_atual.values[0],nconta)
            # Exibe os atributos do novo conta
            print(nova_mov.to_string())
            # Retorna o objeto novo_conta para utilização posterior, caso necessário
            return nova_mov
        else:
            print(f"A Movimentação não pode ser executada - Conta {vnumeroconta} - Limite de {vcontalimite} excedido.")
            return None


    def atualizar_movimentacao(self):
        print("Alterações em Movimentação não podem ser realizadas - Normativa do Banco Central")
        return None

    
    def excluir_movimentacao(self):
        print("Exclusão de Movimentação não pode ser realizada - Normativa do Banco Central")
        return None


    def listar_contas(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.numero
                ,c.tipo
                ,c.saldo
                ,c.limite
                from contas c
                order by c.numero
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_conta(self, oracle:OracleQueries, pnumero:int=None) -> Conta:
        if self.ctrl_conta.verifica_existencia_conta(oracle, pnumero):
            print(f"A Conta {pnumero} informada não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados da conta para o novo movimento criado transformando em um DataFrame
            df_conta = oracle.sqlToDataFrame(f"select id,  numero,  tipo,  saldo,  limite,  id_cliente from contas where numero = {pnumero}")
            # Cria um novo objeto cliente
            nconta = Conta(df_conta.id.values[0], df_conta.numero.values[0], df_conta.tipo.values[0], df_conta.saldo.values[0], df_conta.limite.values[0], df_conta.id_cliente.values[0])
            return nconta