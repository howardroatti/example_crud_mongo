from model.contas import Conta
from datetime import date

class Movimentacao:
    def __init__(self, 
                 id:int=None,
                 data:date=None,
                 descricao:str=None,
                 valor:float=None,
                 saldo_anterior:float=None,
                 saldo_atual:float=None,                 
                 conta:Conta=None
                 ):
        self.set_id(id)
        self.set_data(data)        
        self.set_descricao(descricao)
        self.set_valor(valor)
        self.set_saldo_anterior(saldo_anterior)        
        self.set_saldo_atual(saldo_atual)        
        self.set_conta(conta)

    def set_id(self, id:int):
        self.id = id

    def set_data(self, data:date):
        self.data = data

    def set_descricao(self, descricao:str):
        self.descricao = descricao
    
    def set_valor(self, valor:float):
        self.valor = valor

    def set_saldo_anterior(self, saldo_anterior:float):
        self.saldo_anterior = saldo_anterior

    def set_saldo_atual(self, saldo_atual:float):
        self.saldo_atual = saldo_atual

    def set_conta(self, conta:Conta):
        self.conta = conta                

    def get_id(self) -> int:
        return self.id

    def get_data(self) -> date:
        return self.data

    def get_descricao(self) -> str:
        return self.descricao
    
    def get_valor(self) -> float:
        return self.valor

    def get_saldo_anterior(self) -> float:
        return self.saldo_anterior        
    
    def get_saldo_atual(self) -> float:
        return self.saldo_atual

    def get_conta(self) -> Conta:
        return self.conta

    def to_string(self):
        return f"Movimentação: {self.get_id()} | Data Mov.: {self.get_data()} | Desc.: {self.get_descricao()} | Valor: {self.get_valor()} | Conta: {self.get_conta().get_numero()}"