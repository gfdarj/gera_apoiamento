from classes.aplicacao import Configuracao
from classes.proposicao import Proposicao
import openpyxl

class PlanilhaProjetos:
    def __init__(self):
        self.config = Configuracao()

    def CarregaColunas(self):
        projetos_selecionados = []
        workbook = openpyxl.load_workbook(self.config.arquivo_planilha_de_projetos, keep_vba=True)
        planilha = workbook[self.config.planilha_de_projetos]

        conta = 0
        for linha in planilha.iter_rows():
            if linha[2].value == None and conta > 1:
                break

            if linha[self.config.coluna_reuniao-1].value == self.config.filtro_coluna_reuniao:
                conta += 1
                #print(f"col0: {linha[self.config.coluna_tipo_projeto-1].value} \ncol1: {linha[self.config.coluna_numero_projeto-1].value} \ncol2: {linha[self.config.coluna_autor-1].value} \n col3: {linha[3].value}\n col4: {linha[4].value}")
                #print()  # Passa para a próxima linha após imprimir todas as células da linha atual

                proposicao = Proposicao()
                proposicao.tipo_proposicao = linha[self.config.coluna_tipo_projeto-1].value.strip()
                proposicao.numero = linha[self.config.coluna_numero_projeto-1].value.strip()
                proposicao.ementa = linha[self.config.coluna_ementa-1].value.strip()
                proposicao.autores = linha[self.config.coluna_autor-1].value.strip()
                proposicao.parecer = linha[self.config.coluna_parecer-1].value.strip()
                proposicao.relator = linha[self.config.coluna_relatoria-1].value.strip()

                if "(EP)" in proposicao.numero:
                    proposicao.numero = proposicao.numero.replace("(EP)", "").strip(" ")
                    proposicao.emenda_de_plenario = True
                else:
                    if "EP" in proposicao.numero:
                        proposicao.numero = proposicao.numero.replace("EP", "").strip(" ")
                        proposicao.emenda_de_plenario = True

                num = proposicao.numero.split('/')
                proposicao.numero = num[0]
                proposicao.ano = num[-1]


                projetos_selecionados.append(proposicao)

        #print(f'Projetos selecionadas: {conta}')
        return projetos_selecionados


'''
Testes de execução do módulo.
'''
if __name__ == '__main__':

    print("Teste de execução")
    P = PlanilhaProjetos()
    print("Carregando projetos")
    p = P.CarregaColunas()
    print(f"Projetos selecionados: {len(p)}")
