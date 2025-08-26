from classes.proposicao import Proposicao
from dataclasses import dataclass, asdict
from datetime import datetime
from libs import datas
from pathlib import Path
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm


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
@dataclass
class Edital(Proposicao):
    lista_proposicoes: list = None

    def gera_documento(self, arquivo_modelo, diretorio_geracao):
        documento = Document(arquivo_modelo)
        estilos = documento.styles

        # Texto em geral e linhas em branco
        # Fonte Arial 12, normal
        # Parágrafo justificado, primeira linha com recuo de 1.6 cm
        stl_norm_just_pl16 = cria_estilo(estilos, 'estilo_1', WD_ALIGN_PARAGRAPH.JUSTIFY, 'Arial', Pt(12), negrito=False, recuo_primeira_linha=Cm(1.6), recuo_esquerda=None)

        linha = 1
        relator = ""
        for proposicao in self.lista_proposicoes:

            if relator == "" or relator != proposicao.relator:
                documento.add_paragraph('', style=stl_norm_just_pl16)
                documento.add_paragraph(f"Relator: {proposicao.relator}", style=stl_norm_just_pl16)
                documento.add_paragraph('', style=stl_norm_just_pl16)

            texto = f"{linha}) {'Emendas de Plenário ao Projeto de Lei nº ' if proposicao.emenda_de_plenario else 'Projeto de Lei nº '}{proposicao.numero}/{proposicao.ano}"
            texto += f", do(s) Deputado(s) {proposicao.autores.title()}, que {proposicao.ementa}{"" if proposicao.ementa[-1] == "." else "."}"
            documento.add_paragraph(texto, style=stl_norm_just_pl16)
            documento.add_paragraph('', style=stl_norm_just_pl16)
            linha += 1
            relator = proposicao.relator

        data_formatada = datetime.today().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"edital_{data_formatada}.docx"
        documento.save(diretorio_geracao + nome_arquivo)


'''
Classe Conclusao - Classe para as Conclusões dos Projetos de Lei.
'''
@dataclass
class Conclusao(Proposicao):

    def gera_documento(self, data_sessao, arquivo_modelo, diretorio_geracao):
        documento = Document(arquivo_modelo)
        estilos = documento.styles

        stl_norm_just_pl16 = cria_estilo(estilos, 'estilo_1', WD_ALIGN_PARAGRAPH.JUSTIFY, 'Arial', Pt(12), negrito=False, recuo_primeira_linha=Cm(1.6), recuo_esquerda=None)


        # Geração do documento
        for paragrafo in documento.paragraphs:
            if '{{ NUMERO_PROJETO }}' in paragrafo.text:
                paragrafo.text = paragrafo.text.replace('{{ NUMERO_PROJETO }}', f"{self.numero}/{self.ano}")
            if '{{ REUNIAO }}' in paragrafo.text:
                paragrafo.text = paragrafo.text.replace('{{ REUNIAO }}', self.reuniao)
            if '{{ DATA_REUNIAO }}' in paragrafo.text:
                paragrafo.text = paragrafo.text.replace('{{ DATA_REUNIAO }}', data_sessao)
            if '{{ PARECER }}' in paragrafo.text:
                paragrafo.text = paragrafo.text.replace('{{ PARECER }}', self.parecer)
            if '{{ TIPO_PROPOSICAO }}' in paragrafo.text:
                if self.emenda_de_plenario:
                    tipo_proposicao = f"à(s) Emenda(s) de Plenário ao {self.tipo_proposicao}"
                else:
                    tipo_proposicao = f"ao {self.tipo_proposicao}"
                paragrafo.text = paragrafo.text.replace('{{ TIPO_PROPOSICAO }}', tipo_proposicao)
            if '{{ DATA_REUNIAO_POR_EXTENSO }}' in paragrafo.text:
                paragrafo.text = paragrafo.text.replace('{{ DATA_REUNIAO_POR_EXTENSO }}', datas.data_por_extenso(data_sessao))

            paragrafo.style = stl_norm_just_pl16

        diretorio = Path(diretorio_geracao)
        diretorio.mkdir(parents=True, exist_ok=True)

        nome_arquivo = diretorio_geracao + 'Conclusao ' + self.tipo_proposicao + '_' + self.numero + '-' + self.ano + '.docx'
        documento.save(nome_arquivo)

#        documento.add_paragraph('PROJETO DE LEI', style=stl_neg_cent)
#        documento.add_paragraph('N.º ' + self.numero + ', DE ' + self.ano + '.', style=stl_neg_cent)
        #        documento.add_paragraph('', style=stl_norm_just_pl15)
        #documento.add_paragraph(self.ementa, style=stl_neg_just_esq60)
        #documento.add_paragraph('', style=stl_norm_just_pl15)
        #documento.add_paragraph('A ASSEMBLEIA LEGISLATIVA DO ESTADO DO RIO DE JANEIRO', style=stl_neg_just)
        #documento.add_paragraph('', style=stl_norm_just_pl15)
        #documento.add_paragraph('R E S O L V E:', style=stl_neg_dir)
        #documento.add_paragraph('', style=stl_norm_just_pl15)
        #documento.add_paragraph(self.texto, style=stl_norm_just_pl15)
        #documento.add_paragraph('', style=stl_norm_just_pl15)
        #documento.add_paragraph('Assembleia Legislativa do Estado do Rio de Janeiro, em ' + data_formatada(data_sessao) + '.', style=stl_norm_cent)
        #documento.add_paragraph('', style=stl_norm_just_pl15)
        #if imprime_chancela:
        #    documento.add_picture(arquivo_chancela, width=Cm(6.93), height=Cm(2.95))   # 262x104 pixels
        #    paragrafo_anterior = documento.paragraphs[-1]
        #    paragrafo_anterior.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #documento.add_paragraph('Deputado ' + nome_presidente.upper(), style=stl_neg_cent)
        #documento.add_paragraph(titulo_presidente, style=stl_neg_cent)
        #documento.add_paragraph('', style=stl_norm_just_pl15)
        #if len(self.autores) == 1:
        #    autores = 'Autor: Deputado '
        #else:
        #    autores = 'Autores: Deputados '
        #autores += self.autores + '.'
        #documento.add_paragraph(autores, style=stl_neg_just)
        #documento.add_paragraph('', style=stl_norm_just_pl15)



# Converte Proposição para Edital
def proposicao_para_edital(p: Proposicao) -> Edital:
    return Edital(**asdict(p))


# Converte Proposição para Edital
def proposicao_para_conclusao(p: Proposicao) -> Conclusao:
    return Conclusao(**asdict(p))

