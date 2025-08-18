from aplicacao import Configuracao
import openpyxl

class PlanilhaProjetos:
    config = Configuracao()

    xls = openpyxl.load_workbook(config.arquivo_planilha_de_projetos, keep_vba=True)


