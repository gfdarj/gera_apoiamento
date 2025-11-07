import json
from pathlib import Path
import sys


class Configuracao:

    def __init__(self, ambiente='PROD'):
        try:
            nome_arquivo_json = 'configuracao.json'

            # Caminho absoluto do arquivo de configuração
            config_path = self.resource_path(nome_arquivo_json)
            print(f"🔧 [Config] Usando arquivo de configuração: {config_path}")

            with open(config_path, 'r', encoding='utf-8') as arquivo:
                configuracoes = json.load(arquivo)

            # Converter e exibir todos os caminhos relevantes
            self.banco_dados_proposicoes = self._log_path("Banco de Dados", configuracoes['banco_dados_proposicoes'])
            self.arquivo_modelo_conclusao = self._log_path("Modelo Conclusão", configuracoes['arquivo_modelo_conclusao'])
            self.arquivo_modelo_conclusao_vovo_separado = self._log_path("Modelo Voto Separado", configuracoes['arquivo_modelo_conclusao_voto_separado'])
            self.arquivo_modelo_edital = self._log_path("Modelo Edital", configuracoes['arquivo_modelo_edital'])
            self.diretorio_geracao = self._log_path("Diretório de Geração", configuracoes['diretorio_geracao'])
            self.arquivo_planilha_de_projetos = self._log_path("Planilha de Projetos", configuracoes['arquivo_planilha_de_projetos'])

            # Demais parâmetros
            self.planilha_de_projetos = configuracoes['planilha_de_projetos']
            self.coluna_tipo_projeto = configuracoes['coluna_tipo_projeto']
            self.coluna_ordem = configuracoes['coluna_ordem']
            self.coluna_numero_projeto = configuracoes['coluna_numero_projeto']
            self.coluna_ementa = configuracoes['coluna_ementa']
            self.coluna_autor = configuracoes['coluna_autor']
            self.coluna_parecer = configuracoes['coluna_parecer']
            self.coluna_relatoria = configuracoes['coluna_relatoria']
            self.coluna_reuniao = configuracoes['coluna_reuniao']
            self.filtro_coluna_reuniao = configuracoes['filtro_coluna_reuniao']
            self.url_base = configuracoes['url_base']
            self.presidente_comissao = configuracoes['presidente_comissao']
            self.coluna_parecer_vista = configuracoes['coluna_parecer_vista']
            self.coluna_relatoria_vista = configuracoes['coluna_relatoria_vista']

        except FileNotFoundError as f:
            raise Exception(f"❌ Arquivo de configuração não foi encontrado!\nDetalhes: {f}")

        except Exception as e:
            raise Exception(f"❌ Erro ao carregar configurações: {e}")

    def get_project_root(self, marker_files=("pyproject.toml", "setup.py", ".git", "modelos")) -> Path:
        """
        Retorna o caminho da raiz do projeto Python, subindo diretórios até
        encontrar um dos arquivos/pastas marcadores.
        """
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            for marker in marker_files:
                if (parent / marker).exists():
                    return parent
        return Path(__file__).parent

    def resource_path(self, relative_path: str) -> Path:
        """
        Retorna o caminho absoluto de um recurso do projeto,
        relativo à raiz do projeto.
        Compatível com execução normal e PyInstaller.
        """
        try:
            if hasattr(sys, "_MEIPASS"):
                # Caminho temporário do PyInstaller
                base_path = Path(sys._MEIPASS)
            elif getattr(sys, 'frozen', False):
                # Caminho do executável (.exe)
                base_path = Path(sys.executable).parent
            else:
                # Execução normal (.py)
                base_path = self.get_project_root()
        except Exception:
            base_path = self.get_project_root()

        return (base_path / relative_path).resolve()

    def _log_path(self, label: str, relative_path: str) -> Path:
        """
        Resolve o caminho e exibe no console para debug.
        """
        resolved = self.resource_path(relative_path)
        print(f"📄 [Config] {label}: {resolved}")
        return resolved
