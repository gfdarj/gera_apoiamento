from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import Edital
import argparse


### Coloquei essa linha para que o projeto "veja", na hora de gerar o executável, o pacote de acesso ao
### banco de dados que está no mesmo nível de diretório que este projeto
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proposicoes_bd')))


#
# TESTA OS PARAMETROS
#
def main(numero_inicial: int, tipo: str):
    if not tipo:
        tipo = "link"

    print(f"Número inicial: {numero_inicial}")
    print(f"Tipo: {tipo}")

    IsOK = True

    # Aqui entra a sua lógica principal
    if tipo == "texto":
        print("Gerando edital somente com TEXTO...")
    elif tipo == "link":
        print("Gerando edital com LINK...")
    else:
        print("Tipo inválido! Use 'texto' ou 'link'.")
        IsOK = False

    return IsOK


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera edital com base em parâmetros opcionais.")
    parser.add_argument("numero_inicial", nargs="?", type=int, default=1,
                        help="Número inicial das proposições (inteiro). Padrão = 1")
    parser.add_argument("tipo", nargs="?", type=str, choices=["texto", "link"],
                        help="Tipo de saída ('texto' ou 'link'). Padrão = 'link'")

    args = parser.parse_args()

    if main(args.numero_inicial, args.tipo or ""):

        ordem_inicial = args.numero_inicial

        # Carrega as proposições
        print("Teste de execução")
        P = PlanilhaProjetos(ordem_inicial=int(ordem_inicial))
        print("Carregando projetos")
        proposicoes = P.CarregaColunas()
        print(f"Projetos selecionados: {len(proposicoes)}")


        for d in proposicoes:
            print(f"relator: {d.relator}  ------ ordem: {d.ordem}  ------ numero:{d.numero}/{d.ano}  ----- EP? {d.emenda_de_plenario}")

        config = Configuracao()

        edital = Edital(lista_proposicoes=proposicoes)
        edital.usar_link = args.tipo in (None, "link")
        edital.gera_documento(arquivo_modelo=config.arquivo_modelo_edital, diretorio_geracao=config.diretorio_geracao, banco_dados_proposicoes=config.banco_dados_proposicoes)

        #GRAVA A ORDEM DOS PROJETOS NA PLANILHA
        P.AtualizaOrdemNosProjetos(proposicoes)

    else:
        print("O parâmetro deve ser um número inteiro!\n   Ex: python .\\gera_edital.py 1")

else:
    print("Informe o numeral da ordem inicial para numerar os projetos de lei!\n   Ex: python .\\gera_edital.py 1")


#print(config.arquivo_modelo_edital)
#documento = Document(config.arquivo_modelo_edital)
#estilos = documento.styles

# Texto em geral e linhas em branco
# Fonte Arial 12, normal
# Parágrafo justificado, primeira linha com recuo de 1.6 cm
#stl_norm_just_pl16 = cria_estilo(estilos, 'estilo_1', WD_ALIGN_PARAGRAPH.JUSTIFY, 'Arial', Pt(12), negrito=False, recuo_primeira_linha=Cm(1.6), recuo_esquerda=None)


#linha = 1
#relator = ""
#for proposicao in proposicoes:

#    if relator == "" or relator != proposicao.relator:
#        documento.add_paragraph('', style=stl_norm_just_pl16)
#        documento.add_paragraph(f"Relator: {proposicao.relator}", style=stl_norm_just_pl16)
#        documento.add_paragraph('', style=stl_norm_just_pl16)

#    texto = f"{linha}) {'Emendas de Plenário ao Projeto de Lei nº ' if proposicao.emenda_de_plenario else 'Projeto de Lei nº '}{proposicao.numero}/{proposicao.ano}"
#    texto += f", do(s) Deputado(s) {proposicao.autores.title()}, que {proposicao.ementa}{"" if proposicao.ementa[-1] == "." else "."}"
#    documento.add_paragraph(texto, style=stl_norm_just_pl16)
#    documento.add_paragraph('', style=stl_norm_just_pl16)
#    linha += 1
#    relator = proposicao.relator


#nome_arquivo = 'edital_proximo.docx'
#documento.save(nome_arquivo)





