import tkinter as tk
from tkinter import messagebox, scrolledtext
from classes.aplicacao import Configuracao
from classes.planilha import PlanilhaProjetos
from classes.documento import Edital, Conclusao, proposicao_para_conclusao
from libs.datas import is_valid_date


def gerar_conclusoes():
    data_sessao = entry_data.get().strip()
    reuniao = entry_reuniao.get().strip()
    txt_log.delete(1.0, tk.END)

    # Validação básica
    if not (is_valid_date(data_sessao, "%d/%m/%Y") or is_valid_date(data_sessao, "%d-%m-%Y")):
        messagebox.showerror("Erro de validação", "A data informada está incorreta.\nUse o formato DD/MM/AAAA ou DD-MM-AAAA.")
        return

    if not reuniao:
        messagebox.showerror("Erro de validação", "O campo 'Reunião' é obrigatório.")
        return

    try:
        txt_log.insert(tk.END, "📂 Carregando projetos...\n")
        txt_log.update()

        P = PlanilhaProjetos()
        proposicoes = P.CarregaColunas()
        txt_log.insert(tk.END, f"✅ Projetos carregados: {len(proposicoes)}\n")

        config = Configuracao()

        for d in proposicoes:
            txt_log.insert(tk.END, f"Relator: {d.relator} — nº {d.numero}/{d.ano}\n")
            txt_log.update()

        for proposicao in proposicoes:
            conclusao = proposicao_para_conclusao(proposicao)
            conclusao.arquivo_modelo = config.arquivo_modelo_conclusao
            conclusao.arquivo_modelo_voto_separado = config.arquivo_modelo_conclusao_vovo_separado
            conclusao.diretorio_geracao = config.diretorio_geracao
            conclusao.gera_documento(
                data_sessao=data_sessao,
                reuniao=reuniao
            )

        messagebox.showinfo("Sucesso", "✅ Conclusões geradas com sucesso!")
        txt_log.insert(tk.END, "✅ Conclusões geradas com sucesso!\n")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
        txt_log.insert(tk.END, f"❌ Erro: {e}\n")


# --- Interface gráfica principal ---
janela = tk.Tk()
janela.title("Gerador de Conclusões")
janela.geometry("500x400")

# Labels e entradas
tk.Label(janela, text="Data da Sessão (DD/MM/AAAA ou DD-MM-AAAA):").pack(anchor="w", padx=10, pady=(10, 0))
entry_data = tk.Entry(janela, width=30)
entry_data.pack(padx=10, pady=5)

tk.Label(janela, text="Identificação da Reunião:").pack(anchor="w", padx=10, pady=(10, 0))
entry_reuniao = tk.Entry(janela, width=50)
entry_reuniao.pack(padx=10, pady=5)

# Botão principal
btn_gerar = tk.Button(janela, text="Gerar Conclusões", command=gerar_conclusoes, bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"))
btn_gerar.pack(pady=10)

# Área de log
tk.Label(janela, text="Log de Execução:").pack(anchor="w", padx=10)
txt_log = scrolledtext.ScrolledText(janela, width=60, height=10)
txt_log.pack(padx=10, pady=5, fill="both", expand=True)

# Executa
janela.mainloop()
