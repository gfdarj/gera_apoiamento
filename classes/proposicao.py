from dataclasses import dataclass

'''
Classe Proposicao - Classe base para as proposições.
'''
@dataclass
class Proposicao:
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
