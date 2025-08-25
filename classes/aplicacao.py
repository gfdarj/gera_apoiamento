import json

class Configuracao:

    def __init__(self, ambiente='PROD'):
        try:
            #print(f'{ambiente=}')
            #if ambiente == 'DES':
            #    nome_arquivo_json = 'configuracao_des.json'
            #else:
            nome_arquivo_json = 'configuracao.json'

            with open('./' + nome_arquivo_json, 'r', encoding='utf-8') as arquivo:
                configuracoes = json.load(arquivo)
                self.arquivo_modelo_conclusao = configuracoes['arquivo_modelo_conclusao']
                self.arquivo_modelo_edital = configuracoes['arquivo_modelo_edital']
                self.diretorio_geracao = configuracoes['diretorio_geracao']
                self.arquivo_planilha_de_projetos = configuracoes['arquivo_planilha_de_projetos']
                self.planilha_de_projetos = configuracoes['planilha_de_projetos']
                self.coluna_tipo_projeto = configuracoes['coluna_tipo_projeto']
                self.coluna_numero_projeto = configuracoes['coluna_numero_projeto']
                self.coluna_ementa = configuracoes['coluna_ementa']
                self.coluna_autor = configuracoes['coluna_autor']
                self.coluna_parecer = configuracoes['coluna_parecer']
                self.coluna_relatoria = configuracoes['coluna_relatoria']
                self.coluna_reuniao = configuracoes['coluna_reuniao']
                self.filtro_coluna_reuniao = configuracoes['filtro_coluna_reuniao']
                self.url_base = configuracoes['url_base']

        except Exception as e:
            print(f'Erro: {e}')
            exit(1)

