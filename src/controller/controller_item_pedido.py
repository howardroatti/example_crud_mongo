import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.itens_pedido import ItemPedido
from model.produtos import Produto
from model.pedidos import Pedido

from controller.controller_produto import Controller_Produto
from controller.controller_pedido import Controller_Pedido

from conexion.mongo_queries import MongoQueries

class Controller_Item_Pedido:
    def __init__(self):
        self.ctrl_produto = Controller_Produto()
        self.ctrl_pedido = Controller_Pedido()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_item_pedido(self) -> ItemPedido:
        # Cria uma nova conexão com o banco
        self.mongo.connect()
        
        # Lista os pedido existentes para inserir no item de pedido
        self.relatorio.get_relatorio_pedidos()
        codigo_pedido = int(str(input("Digite o número do Pedido: ")))
        pedido = self.valida_pedido(codigo_pedido)
        if pedido == None:
            return None

        # Lista os produtos existentes para inserir no item de pedido
        self.relatorio.get_relatorio_produtos()
        codigo_produto = int(str(input("Digite o código do Produto: ")))
        produto = self.valida_produto(codigo_produto)
        if produto == None:
            return None

        # Solicita a quantidade de itens do pedido para o produto selecionado
        quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))
        # Solicita o valor unitário do produto selecionado
        valor_unitario = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))

        proximo_item_pedido = self.mongo.db["itens_pedido"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$itens_pedido', 
                                                            'proximo_item_pedido': {
                                                                '$max': '$codigo_item_pedido'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_item_pedido': {
                                                                '$sum': [
                                                                    '$proximo_item_pedido', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_item_pedido = int(list(proximo_item_pedido)[0]['proximo_item_pedido'])
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo_item_pedido=proximo_item_pedido, valor_unitario=valor_unitario, quantidade=quantidade, codigo_pedido=int(pedido.get_codigo_pedido()), codigo_produto=int(produto.get_codigo()))
        # Insere e Recupera o código do novo item de pedido
        id_item_pedido = self.mongo.db["itens_pedido"].insert_one(data)
        # Recupera os dados do novo item de pedido criado transformando em um DataFrame
        df_item_pedido = self.recupera_item_pedido(id_item_pedido.inserted_id)
        # Cria um novo objeto Item de Pedido
        novo_item_pedido = ItemPedido(df_item_pedido.codigo_item_pedido.values[0], df_item_pedido.quantidade.values[0], df_item_pedido.valor_unitario.values[0], pedido, produto)
        # Exibe os atributos do novo Item de Pedido
        print(novo_item_pedido.to_string())
        self.mongo.close()
        # Retorna o objeto novo_item_pedido para utilização posterior, caso necessário
        return novo_item_pedido

    def atualizar_item_pedido(self) -> ItemPedido:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        codigo_item_pedido = int(input("Código do Item de Pedido que irá alterar: "))        

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_item_pedido(codigo_item_pedido):

            # Lista os pedido existentes para inserir no item de pedido
            self.relatorio.get_relatorio_pedidos()
            codigo_pedido = int(str(input("Digite o número do Pedido: ")))
            pedido = self.valida_pedido(codigo_pedido)
            if pedido == None:
                return None

            # Lista os produtos existentes para inserir no item de pedido
            self.relatorio.get_relatorio_produtos()
            codigo_produto = int(str(input("Digite o código do Produto: ")))
            produto = self.valida_produto(codigo_produto)
            if produto == None:
                return None

            # Solicita a quantidade de itens do pedido para o produto selecionado
            quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))
            # Solicita o valor unitário do produto selecionado
            valor_unitario = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))

            # Atualiza o item de pedido existente
            self.mongo.db["itens_pedido"].update_one({"codigo_item_pedido": codigo_item_pedido},
                                                     {"$set": {"quantidade": quantidade,
                                                               "valor_unitario":  valor_unitario,
                                                               "codigo_pedido": int(pedido.get_codigo_pedido()),
                                                               "codigo_produto": int(produto.get_codigo())
                                                          }
                                                     })
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_item_pedido = self.recupera_item_pedido_codigo(codigo_item_pedido)
            # Cria um novo objeto Item de Pedido
            item_pedido_atualizado = ItemPedido(df_item_pedido.codigo_item_pedido.values[0], df_item_pedido.quantidade.values[0], df_item_pedido.valor_unitario.values[0], pedido, produto)
            # Exibe os atributos do item de pedido
            print(item_pedido_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return item_pedido_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_item_pedido} não existe.")
            return None

    def excluir_item_pedido(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        codigo_item_pedido = int(input("Código do Item de Pedido que irá excluir: "))        

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_item_pedido(codigo_item_pedido):            
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_item_pedido = self.recupera_item_pedido_codigo(codigo_item_pedido)
            pedido = self.valida_pedido(int(df_item_pedido.codigo_pedido.values[0]))
            produto = self.valida_produto(int(df_item_pedido.codigo_produto.values[0]))
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o item de pedido {codigo_item_pedido} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome o item de pedido da tabela
                self.mongo.db["itens_pedido"].delete_one({"codigo_item_pedido": codigo_item_pedido})
                # Cria um novo objeto Item de Pedido para informar que foi removido
                item_pedido_excluido = ItemPedido(df_item_pedido.codigo_item_pedido.values[0], 
                                                  df_item_pedido.quantidade.values[0], 
                                                  df_item_pedido.valor_unitario.values[0], 
                                                  pedido, 
                                                  produto)
                self.mongo.close()
                # Exibe os atributos do produto excluído
                print("Item do Pedido Removido com Sucesso!")
                print(item_pedido_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_item_pedido} não existe.")

    def verifica_existencia_item_pedido(self, codigo:int=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = self.recupera_item_pedido_codigo(codigo=codigo)
        return df_pedido.empty

    def recupera_item_pedido(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = pd.DataFrame(list(self.mongo.db["itens_pedido"].find({"_id": _id}, {"codigo_item_pedido":1, "quantidade": 1, "valor_unitario": 1, "codigo_pedido": 1, "codigo_produto": 1, "_id": 0})))
        return df_pedido

    def recupera_item_pedido_codigo(self, codigo:int=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = pd.DataFrame(list(self.mongo.db["itens_pedido"].find({"codigo_item_pedido": codigo}, {"codigo_item_pedido":1, 
                                                                                                          "quantidade": 1, 
                                                                                                          "valor_unitario": 1, 
                                                                                                          "codigo_pedido": 1, 
                                                                                                          "codigo_produto": 1, 
                                                                                                          "_id": 0})))
        return df_pedido

    def valida_pedido(self, codigo_pedido:int=None) -> Pedido:
        if self.ctrl_pedido.verifica_existencia_pedido(codigo_pedido, external=True):
            print(f"O pedido {codigo_pedido} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_pedido = self.ctrl_pedido.recupera_pedido_codigo(codigo_pedido, external=True)
            cliente = self.ctrl_pedido.valida_cliente(df_pedido.cpf.values[0])
            fornecedor = self.ctrl_pedido.valida_fornecedor(df_pedido.cnpj.values[0])
            # Cria um novo objeto cliente
            pedido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
            return pedido

    def valida_produto(self, codigo_produto:int=None) -> Produto:
        if self.ctrl_produto.verifica_existencia_produto(codigo_produto, external=True):
            print(f"O produto {codigo_produto} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_produto = self.ctrl_produto.recupera_produto_codigo(codigo_produto, external=True)
            # Cria um novo objeto Produto
            produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            return produto