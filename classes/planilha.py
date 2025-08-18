from aplicacao import Configuracao
import openpyxl

class PlanilhaProjetos:
    def __init__(self):
        self.config = Configuracao()

    def AbrePlanilha(self):
        xls = openpyxl.load_workbook(self.config.arquivo_planilha_de_projetos, keep_vba=True)
        xls.active = self.config.planilha_de_projetos
        return xls

