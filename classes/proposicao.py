
'''
Classe Proposicao - Classe base para as proposições.
'''
class Proposicao:
    def __init__(self, numero='', ano=''):
        self.numero = numero
        self.ano = ano
        self.tipo_proposicao = ''
        self.ementa = ''
        self.texto = ''
        self.reuniao = ''
        self.relator = ''
        self.autores = None
        self.parecer = None

