from proposicao import Proposicao


class ProjetoLei(Proposicao):

    def __init__(self, numero='', ano=''):
        super().__init__(numero, ano)

    def gera_documento(self, data_sessao, arquivo_modelo, imprime_chancela, arquivo_chancela, nome_presidente, titulo_presidente, diretorio_geracao):
        return ""


class ProjetoLeiComplementar(Proposicao):

    def __init__(self, numero='', ano=''):
        super().__init__(numero, ano)

    def gera_documento(self, data_sessao, arquivo_modelo, imprime_chancela, arquivo_chancela, nome_presidente, titulo_presidente, diretorio_geracao):
        return ""

