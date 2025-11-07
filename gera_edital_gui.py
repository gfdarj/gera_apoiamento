import tkinter as tk
from tkinter import messagebox, scrolledtext
from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import Edital
import sys, os

# Adiciona o pacote proposicoes_bd (no mesmo nível do projeto)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proposicoes_bd')))


# ---------- Redirecionador de saída para o console gráfico ----------
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass


# ---------- Lógica principal ----------
def gerar_edital(numero_inicial: int, tipo: str, console: tk.Text):
    """Executa a geração do edital com redirecionamento para o console Tkinter."""

    def log(msg):
        console.config(state=tk.NORMAL)
        console.insert(tk.END, msg + "\n")
        console.see(tk.END)
        console.config(state=tk.DISABLED)
        console.update_idletasks()

    if not tipo:
        tipo = "link"

    log(f"➡ Número inicial: {numero_inicial}")
    log(f"➡ Tipo: {tipo}")

    if tipo not in ("texto", "link"):
        messagebox.showerror("Erro", "Tipo inválido! Use 'texto' ou 'link'.")
        return

    try:
        log("📂 Teste de execução")
        P = PlanilhaProjetos(ordem_inicial=int(numero_inicial))
        log("📘 Carregando projetos...")
        proposicoes = P.CarregaColunas()
        log(f"✅ Projetos selecionados: {len(proposicoes)}")

        for d in proposicoes:
            log(f"Relator: {d.relator}  ------ ordem: {d.ordem}  ------ número:{d.numero}/{d.ano}  ----- EP? {d.emenda_de_plenario}")

        config = Configuracao()

        edital = Edital(lista_proposicoes=proposicoes)
        edital.usar_link = tipo == "link"

        edital.gera_documento(
            arquivo_modelo=config.arquivo_modelo_edital,
            diretorio_geracao=config.diretorio_geracao,
            banco_dados_proposicoes=config.banco_dados_proposicoes
        )

        # Atualiza a planilha com as ordens
        P.AtualizaOrdemNosProjetos(proposicoes)

        log("✅ Edital gerado com sucesso!")
        messagebox.showinfo("Sucesso", "✅ Edital gerado com sucesso!")

    except Exception as e:
        log(f"❌ Erro: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o edital:\n{e}")


# ---------- Interface gráfica ----------
def criar_interface():
    root = tk.Tk()
    root.title("Gerador de Edital")
    root.geometry("700x500")
    root.resizable(False, False)

    # Título
    tk.Label(root, text="Gerador de Edital", font=("Arial", 14, "bold")).pack(pady=10)

    # Campo número inicial
    frame_inputs = tk.Frame(root)
    frame_inputs.pack(pady=5)

    tk.Label(frame_inputs, text="Número inicial (inteiro):").grid(row=0, column=0, padx=5, pady=5)
    entry_numero = tk.Entry(frame_inputs, width=10)
    entry_numero.insert(0, "1")  # valor padrão
    entry_numero.grid(row=0, column=1, padx=5)

    # Opção tipo
    tk.Label(frame_inputs, text="Tipo de saída:").grid(row=0, column=2, padx=15)
    tipo_var = tk.StringVar(value="link")

    frame_tipo = tk.Frame(frame_inputs)
    frame_tipo.grid(row=0, column=3)
    tk.Radiobutton(frame_tipo, text="Link", variable=tipo_var, value="link").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(frame_tipo, text="Texto", variable=tipo_var, value="texto").pack(side=tk.LEFT, padx=5)

    # Botão gerar
    def ao_clicar():
        numero_str = entry_numero.get().strip()
        tipo = tipo_var.get()

        if not numero_str.isdigit():
            messagebox.showerror("Erro de validação", "O número inicial deve ser um número inteiro.")
            return

        console_output.config(state=tk.NORMAL)
        console_output.delete(1.0, tk.END)
        console_output.config(state=tk.DISABLED)

        gerar_edital(int(numero_str), tipo, console_output)

    tk.Button(root, text="Gerar Edital", command=ao_clicar, bg="#4CAF50", fg="white", width=20).pack(pady=10)

    # Console de saída
    tk.Label(root, text="Saída de execução:", font=("Arial", 10, "bold")).pack()
    console_output = scrolledtext.ScrolledText(root, height=18, width=85, state=tk.DISABLED, font=("Consolas", 9))
    console_output.pack(pady=5)

    # Redireciona o print() padrão para o console gráfico
    sys.stdout = TextRedirector(console_output)
    sys.stderr = TextRedirector(console_output)

    root.mainloop()


if __name__ == "__main__":
    criar_interface()
