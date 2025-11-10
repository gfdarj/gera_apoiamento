import sys
import os
import io
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import Edital

# Adiciona o caminho para o pacote proposicoes_bd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proposicoes_bd')))


class RedirectText:
    """Classe auxiliar para redirecionar prints ao Text widget"""
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
        self.output.update_idletasks()

    def flush(self):
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Edital")
        self.geometry("720x520")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        # ---- Parâmetros ----
        ttk.Label(frm, text="Número inicial:").grid(column=0, row=0, sticky="w", pady=5)
        self.numero_var = tk.StringVar(value="1")
        ttk.Entry(frm, textvariable=self.numero_var, width=10).grid(column=1, row=0, sticky="w")

        ttk.Label(frm, text="Tipo:").grid(column=0, row=1, sticky="w", pady=5)
        self.tipo_var = tk.StringVar(value="link")
        ttk.Combobox(frm, textvariable=self.tipo_var, values=["texto", "link"], width=10, state="readonly").grid(column=1, row=1, sticky="w")

        ttk.Label(frm, text="Ordenação:").grid(column=0, row=2, sticky="w", pady=5)
        self.ordenacao_var = tk.StringVar(value="comum")
        ttk.Combobox(frm, textvariable=self.ordenacao_var, values=["comum", "nenhuma"], width=10, state="readonly").grid(column=1, row=2, sticky="w")

        ttk.Button(frm, text="Gerar Edital", command=self.executar).grid(column=0, row=3, columnspan=2, pady=10)

        # ---- Console ----
        ttk.Label(frm, text="Saída do processo:").grid(column=0, row=4, sticky="w")
        self.console = scrolledtext.ScrolledText(frm, width=85, height=20, wrap=tk.WORD, state=tk.NORMAL)
        self.console.grid(column=0, row=5, columnspan=3, pady=10)
        self.console.configure(font=("Consolas", 9))

        # Redirecionar saída padrão
        self.redirect = RedirectText(self.console)
        sys.stdout = self.redirect
        sys.stderr = self.redirect

    def executar(self):
        try:
            self.console.delete(1.0, tk.END)
            numero_inicial = int(self.numero_var.get())
            tipo = self.tipo_var.get()
            ordenacao = self.ordenacao_var.get()

            print(f"\n==============================")
            print(f"▶ Iniciando geração do edital")
            print(f"==============================")
            print(f"Número inicial: {numero_inicial}")
            print(f"Tipo: {tipo}")
            print(f"Ordenação: {ordenacao}\n")

            if not self.main(numero_inicial, tipo, ordenacao):
                messagebox.showerror("Erro", "Parâmetros inválidos. Verifique o console.")
            else:
                messagebox.showinfo("Concluído", "✅ Geração do edital finalizada com sucesso.")

        except ValueError:
            messagebox.showerror("Erro", "O número inicial deve ser um valor inteiro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

    def main(self, numero_inicial: int, tipo: str, ordenacao: str):
        if not tipo:
            tipo = "link"
        if not ordenacao:
            ordenacao = "comum"

        IsOK = True

        if tipo not in ("texto", "link"):
            print("❌ Tipo inválido! Use 'texto' ou 'link'.")
            IsOK = False

        if ordenacao not in ("comum", "nenhuma"):
            print("❌ Ordenação inválida! Use 'comum' ou 'nenhuma'.")
            IsOK = False

        if not IsOK:
            return False

        # ---- Execução principal ----
        print("🔧 Teste de execução...")
        P = PlanilhaProjetos(ordem_inicial=int(numero_inicial), ordenacao=ordenacao)
        print("📄 Carregando projetos...")
        proposicoes = P.CarregaColunas()
        print(f"✅ Projetos selecionados: {len(proposicoes)}")

        for d in proposicoes:
            print(f"Relator: {d.relator}  | Ordem: {d.ordem}  | Número: {d.numero}/{d.ano}  | EP? {d.emenda_de_plenario}")

        config = Configuracao()

        edital = Edital(lista_proposicoes=proposicoes)
        edital.usar_link = tipo in (None, "link")
        edital.gera_documento(
            arquivo_modelo=config.arquivo_modelo_edital,
            diretorio_geracao=config.diretorio_geracao,
            banco_dados_proposicoes=config.banco_dados_proposicoes
        )

        P.AtualizaOrdemNosProjetos(proposicoes)
        print("\n✅ Processo concluído com sucesso!")
        return True


if __name__ == "__main__":
    app = App()
    app.mainloop()
