from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from classes.proposicao import Proposicao

def cria_estilo(lista_estilos, nome_estilo, alinhamento, fonte, tamanho, negrito=False, recuo_primeira_linha=None, recuo_esquerda=None):
    '''
    Cria um estilo de parágrafo para o documento e adiciona à folha de estilos.

    :param lista_estilos: folha de estilos à qual o novo estilo será adicionado.
    :param nome_estilo: nome do novo estilo.
    :param alinhamento: alinhamento do parágrafo (justificado, centralizado, à direita, etc.).
    :param fonte: nome da fonte a ser utilizada.
    :param tamanho: tamanho da fonte.
    :param negrito: booleano indicando se a fonte é em negrito ou não.
    :param recuo_primeira_linha: tamanho do recuo da primeira linha do parágrafo (defalut None).
    :param recuo_esquerda: tamanho do recuo à esquerda do parágrafo (default None).
    '''
    estilo = lista_estilos.add_style(nome_estilo, WD_STYLE_TYPE.PARAGRAPH)
    estilo.paragraph_format.alignment = alinhamento
    estilo.font.name = fonte
    estilo.font.size = tamanho
    estilo.font.bold = negrito
    if recuo_primeira_linha:
        estilo.paragraph_format.first_line_indent = recuo_primeira_linha
    if recuo_esquerda:
        estilo.paragraph_format.left_indent = recuo_esquerda
    return estilo



'''
Classe ProjetoLei - Classe para os Projetos de Lei.
'''
class Conclusao(Proposicao):

    def __init__(self, numero='', ano=''):
        super().__init__(numero, ano)

    def gera_documento(self, data_sessao, arquivo_modelo, imprime_chancela, arquivo_chancela, nome_presidente, titulo_presidente, diretorio_geracao):
        documento = Document(arquivo_modelo)
        estilos = documento.styles
        # Número do PL e assinatura do Presidente
        # Fonte Arial 10, negrito
        # Parágrafo centralizado
        stl_neg_cent = cria_estilo(estilos, 'estilo_1', WD_ALIGN_PARAGRAPH.CENTER, 'Arial', Pt(10), negrito=True)
        # Texto em geral e linhas em branco
        # Fonte Arial 10, normal
        # Parágrafo justificado, primeira linha com recuo de 1.5 cm
        stl_norm_just_pl15 = cria_estilo(estilos, 'estilo_3', WD_ALIGN_PARAGRAPH.JUSTIFY, 'Arial', Pt(10), negrito=False, recuo_primeira_linha=Cm(1.5))
        # Ementa
        # Fonte Arial 10, negrito
        # Parágrafo justificado, recuo à esquerda de 6.0 cm
        stl_neg_just_esq60 = cria_estilo(estilos, 'estilo_4', WD_ALIGN_PARAGRAPH.JUSTIFY, 'Arial', Pt(10), negrito=True, recuo_esquerda=Cm(6.0))
        # Texto "A ASSEMBLEIA LEGISLATIVA DO ESTADO DO RIO DE JANEIRO" e autoria
        # Fonte Arial 10, negrito
        # Parágrafo justificado
        stl_neg_just = cria_estilo(estilos, 'estilo_5', WD_ALIGN_PARAGRAPH.JUSTIFY, 'Arial', Pt(10), negrito=True)
        # Texto "R E S O L V E:"
        # Fonte Arial 10, negrito
        # Parágrafo alinhado à direita
        stl_neg_dir = cria_estilo(estilos, 'estilo_6', WD_ALIGN_PARAGRAPH.RIGHT, 'Arial', Pt(10), negrito=True)
        # Local e data
        # Fonte Arial 10, normal
        # Parágrafo centralizado
        stl_norm_cent = cria_estilo(estilos, 'estilo_7', WD_ALIGN_PARAGRAPH.CENTER, 'Arial', Pt(10), negrito=False)
        # Geração do documento
        documento.add_paragraph('PROJETO DE LEI', style=stl_neg_cent)
        documento.add_paragraph('N.º ' + self.numero + ', DE ' + self.ano + '.', style=stl_neg_cent)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        documento.add_paragraph(self.ementa, style=stl_neg_just_esq60)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        documento.add_paragraph('A ASSEMBLEIA LEGISLATIVA DO ESTADO DO RIO DE JANEIRO', style=stl_neg_just)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        documento.add_paragraph('R E S O L V E:', style=stl_neg_dir)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        documento.add_paragraph(self.texto, style=stl_norm_just_pl15)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        documento.add_paragraph('Assembleia Legislativa do Estado do Rio de Janeiro, em ' + data_formatada(data_sessao) + '.', style=stl_norm_cent)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        if imprime_chancela:
            documento.add_picture(arquivo_chancela, width=Cm(6.93), height=Cm(2.95))   # 262x104 pixels
            paragrafo_anterior = documento.paragraphs[-1]
            paragrafo_anterior.alignment = WD_ALIGN_PARAGRAPH.CENTER
        documento.add_paragraph('Deputado ' + nome_presidente.upper(), style=stl_neg_cent)
        documento.add_paragraph(titulo_presidente, style=stl_neg_cent)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        if len(self.autores) == 1:
            autores = 'Autor: Deputado '
        else:
            autores = 'Autores: Deputados '
        autores += self.autores + '.'
        documento.add_paragraph(autores, style=stl_neg_just)
        documento.add_paragraph('', style=stl_norm_just_pl15)
        nome_arquivo = diretorio_geracao + 'PL_' + self.numero + '-' + self.ano + '.docx'
        documento.save(nome_arquivo)



