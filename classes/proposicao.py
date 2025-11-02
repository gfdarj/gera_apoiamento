from dataclasses import dataclass

'''
Classe Proposicao - Classe base para as proposições.
'''
@dataclass
class Proposicao:
    ordem: int = 0
    numero: str = ''
    ano: str = ''
    tipo_proposicao: str = ''
    ementa: str = ''
    texto: str = ''
    reuniao: str = ''
    relator: str = ''
    autores: str = None
    parecer: str = None
    emenda_de_plenario: bool = False
    linha_da_planilha: int = None


    def classifica_tipo_proposicao(self, nome_resumido=False):
        if "PROJETO" in self.tipo_proposicao.upper() and "LEI" in self.tipo_proposicao.upper() and "COMPL" in self.tipo_proposicao.upper():
            tipo_resumido = "PLC"
            tipo = "Projeto de Lei Complementar"
        else:
            if "PROJETO" in self.tipo_proposicao.upper() and "LEI" in self.tipo_proposicao.upper():
                tipo_resumido = "PL"
                tipo = "Projeto de Lei"

        if nome_resumido:
            return tipo_resumido
        else:
            return tipo

