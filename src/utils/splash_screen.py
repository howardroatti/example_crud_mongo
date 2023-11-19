from utils import config

class SplashScreen:

    def __init__(self):
        self.created_by = '''
        #        ANTHONY MAHYHAKER SILVA
        #        CIRO MASSARIOL DE ARAUJO
        #        IVIE ALVARINO FAÉ DE OLIVEIRA E SILVA
        #        PEDRO HENRIQUE SOSSAI CAMATA''' 

        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documents_count(self, collection_name):
        # Retorna o total de registros computado pela query
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #              SISTEMA DE GESTÃO BANCÁRIA                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - CLIENTES:         {str(self.get_documents_count(collection_name="clientes")).rjust(5)}
        #      2 - CONTAS:           {str(self.get_documents_count(collection_name="contas")).rjust(5)}
        #      3 - MOVIMENTAÇÕES:    {str(self.get_documents_count(collection_name="movimentacoes")).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """