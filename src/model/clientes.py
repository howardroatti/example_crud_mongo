class Cliente:
    def __init__(self,
                 id:int=None,
                 CPF:str=None, 
                 nome:str=None,
                 endereco:str=None,
                 telefone:str=None,
                ):
        self.set_id(id)
        self.set_CPF(CPF)
        self.set_nome(nome)
        self.set_endereco(endereco)
        self.set_telefone(telefone)

    def set_id(self, id:int):
        self.id = id

    def set_CPF(self, CPF:str):
        self.CPF = CPF

    def set_nome(self, nome:str):
        self.nome = nome

    def set_endereco(self, endereco:str):
        self.endereco = endereco

    def set_telefone(self, telefone:str):
        self.telefone = telefone

    def get_id(self) -> int:
        return id

    def get_CPF(self) -> str:
        return self.CPF

    def get_nome(self) -> str:
        return self.nome
    
    def get_endereco(self) -> str:
        return self.endereco

    def get_telefone(self) -> str:
        return self.telefone

    def to_string(self) -> str:
        return f"CPF: {self.get_CPF()} | Nome: {self.get_nome()} | Endereço: {self.get_endereco()} | Telefone: {self.get_telefone()}"