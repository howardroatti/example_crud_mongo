from datetime import date
from model.clientes import Cliente
##from model.fornecedores import Fornecedor

class Conta:
    def __init__(self,
                 id:int=None, 
                 numero:int=None,
                 tipo:str=None,
                 saldo:float=None,
                 limite:float=None,
                 cliente:Cliente= None
                 ):
        self.set_id(id)
        self.set_numero(numero)
        self.set_tipo(tipo)
        self.set_saldo(saldo)
        self.set_limite(limite)
        self.set_cliente(cliente)
    
    def set_id(self, id:int):
        self.id = id

    def set_numero(self, numero:int):
        self.numero = numero

    def set_tipo(self, tipo:str):
        self.tipo = tipo

    def set_saldo(self, saldo:float):
        self.saldo = saldo        

    def set_limite(self, limite:float):
        self.limite = limite

    def set_cliente(self, cliente:Cliente):
        self.cliente = cliente

    def get_id(self) -> int:
        return self.id

    def get_numero(self) -> int:
        return self.numero

    def get_tipo(self) -> str:
        return self.tipo

    def get_saldo(self) -> float:
        return self.saldo
    
    def get_limite(self) -> float:
        return self.limite
    
    def get_cliente(self) -> Cliente:
        return self.cliente
    
    def to_string(self) -> str:
        return f"Conta n: {self.get_numero()} | Tipo Conta: {self.get_tipo()} | Saldo: {self.get_saldo()} | Limite Conta: {self.get_limite()}"