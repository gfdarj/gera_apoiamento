import json
from pathlib import Path
import sys
import os


class Configuracao:
    def __init__(self, ambiente='PROD'):
        try:
            nome_arquivo_json = 'configuracao.json'

            # Caminho absoluto do arquivo de configuração (corrigido para funcionar no .exe)
            config_path = self._find_config_path(nome_arquivo_json)
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

    # =====================================================
    # MÉTODOS AUXILIARES
    # =====================================================

    def _find_config_path(self, filename: str) -> Path:
        """
        Tenta localizar o arquivo de configuração no local correto:
        - Mesmo diretório do executável (.exe) quando empacotado
        - Diretório atual ou raiz do projeto em modo de desenvolvimento
        """
        if getattr(sys, 'frozen', False):
            # Quando está empacotado (.exe)
            exe_dir = Path(sys.executable).parent
            candidate = exe_dir / filename
            if candidate.exists():
                return candidate.resolve()
            else:
                # fallback: tenta também o diretório de trabalho
                cwd_candidate = Path(os.getcwd()) / filename
                if cwd_candidate.exists():
                    return cwd_candidate.resolve()
        else:
            # Execução normal (.py)
            dev_candidate = Path(__file__).parent / filename
            if dev_candidate.exists():
                return dev_candidate.resolve()

        # fallback final: procura recursivamente
        for parent in Path(__file__).resolve().parents:
            possible = parent / filename
            if possible.exists():
                return possible.resolve()

        raise FileNotFoundError(f"Arquivo {filename} não encontrado em nenhum dos caminhos conhecidos.")

    def get_project_root(self, marker_files=("pyproject.toml", "setup.py", ".git", "modelos")) -> Path:
        """Identifica a raiz do projeto, usada em modo de desenvolvimento"""
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            for marker in marker_files:
                if (parent / marker).exists():
                    return parent
        return Path(__file__).parent

    def resource_path(self, relative_path: str) -> Path:
        """
        Retorna o caminho absoluto de um recurso do projeto,
        relativo à raiz do projeto ou ao diretório do executável.
        Compatível com execução normal e PyInstaller.
        """
        try:
            if hasattr(sys, "_MEIPASS"):
                # PyInstaller em modo onefile
                base_path = Path(sys._MEIPASS)
            elif getattr(sys, 'frozen', False):
                # Diretório onde está o executável
                base_path = Path(sys.executable).parent
            else:
                # Execução normal
                base_path = self.get_project_root()
        except Exception:
            base_path = self.get_project_root()

        full_path = (base_path / relative_path).resolve()

        # 🔍 Verifica se o arquivo existe, senão tenta buscar no mesmo diretório do executável
        if not full_path.exists():
            exe_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path.cwd()
            alt_path = (exe_dir / Path(relative_path).name).resolve()
            if alt_path.exists():
                print(f"⚙️ [Config] Recurso '{relative_path}' não encontrado em {base_path}, usando {alt_path}")
                return alt_path

        return full_path


    def _log_path(self, label: str, relative_path: str) -> Path:
        """Resolve o caminho e exibe no console para debug."""
        resolved = self.resource_path(relative_path)
        print(f"📄 [Config] {label}: {resolved}")
        return resolved
