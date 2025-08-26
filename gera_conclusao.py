from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import cria_estilo, Edital, Conclusao, proposicao_para_conclusao
import sys
from libs.datas import is_valid_date


if len(sys.argv) > 1:
    data_sessao = sys.argv[1]

    if is_valid_date(data_sessao, "%d/%m/%Y") or is_valid_date(data_sessao, "%d-%m-%Y"):

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
            conclusao.gera_documento(data_sessao=data_sessao, arquivo_modelo=config.arquivo_modelo_conclusao,
                                     diretorio_geracao=config.diretorio_geracao)

    else:
        print("A data informada está errada.\n   Ex: python .\\gera_conclusao.py dia-mes-ano")

else:
    print("Informe a Data da Sessão!\n   Ex: python .\\gera_conclusao.py dia-mes-ano")

