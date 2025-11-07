import argparse
from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import Edital, Conclusao, proposicao_para_conclusao
from libs.datas import is_valid_date


def main(data_sessao: str, reuniao: str):
    # Validação manual adicional (além do argparse)
    if not (is_valid_date(data_sessao, "%d/%m/%Y") or is_valid_date(data_sessao, "%d-%m-%Y")):
        print("❌ A data informada está incorreta. Use o formato DD/MM/AAAA ou DD-MM-AAAA.")
        return

    if not reuniao:
        print("❌ O campo de reunião é obrigatório.")
        return

    try:
        # Carrega os projetos
        print("📂 Carregando projetos...")
        P = PlanilhaProjetos()
        proposicoes = P.CarregaColunas()
        print(f"✅ Projetos carregados: {len(proposicoes)}")

        for d in proposicoes:
            print(f"Relator: {d.relator}  ------ número:{d.numero}/{d.ano}  ----- EP? {d.emenda_de_plenario}")

        # Gera conclusões
        config = Configuracao()
        for proposicao in proposicoes:
            conclusao = proposicao_para_conclusao(proposicao)
            conclusao.arquivo_modelo = config.arquivo_modelo_conclusao
            conclusao.arquivo_modelo_voto_separado = config.arquivo_modelo_conclusao_vovo_separado
            conclusao.diretorio_geracao = config.diretorio_geracao
            conclusao.gera_documento(
                data_sessao=data_sessao,
                reuniao=reuniao
            )

        print("✅ Conclusões geradas com sucesso.")

    except Exception as e:
        print(f"❌ Ocorreu um erro:\n{e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gera as conclusões das proposições (Projetos de Lei)."
    )
    parser.add_argument(
        "data_sessao",
        type=str,
        help="Data da sessão (formato DD/MM/AAAA ou DD-MM-AAAA)."
    )
    parser.add_argument(
        "reuniao",
        type=str,
        help="Identificação da reunião (ex: '1ª Reunião Extraordinária')."
    )

    args = parser.parse_args()
    main(args.data_sessao, args.reuniao)
