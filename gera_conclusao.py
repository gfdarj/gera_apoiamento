from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import cria_estilo, Edital, Conclusao, proposicao_para_conclusao
import locale
from docx import Document
from datetime import datetime
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm


# Carrega as proposições
print("Teste de execução")
P = PlanilhaProjetos()
print("Carregando projetos")
proposicoes = P.CarregaColunas()
print(f"Projetos selecionados: {len(proposicoes)}")



for d in proposicoes:
    print(f"relator: {d.relator}  ------ numero:{d.numero}/{d.ano}  ----- EP? {d.emenda_de_plenario}")


config = Configuracao()

for proposicao in proposicoes:
    conclusao = proposicao_para_conclusao(proposicao)
    conclusao.gera_documento(arquivo_modelo=config.arquivo_modelo_edital, diretorio_geracao=config.diretorio_geracao)

