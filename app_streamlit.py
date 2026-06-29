import streamlit as st
import sys
import io
import json
import zipfile
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────
# Configuração de página
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistema de Documentos · CCJ",
    page_icon="⚖️",
    layout="centered",
)

# ──────────────────────────────────────────────────────────
# CSS global
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
    h1, h2, h3 { font-family: 'Merriweather', serif !important; }

    /* ── Cabeçalho ── */
    .main-header {
        background: linear-gradient(135deg, #1a3a5c 0%, #2c5f8a 100%);
        padding: 1.4rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .main-header-left h1 {
        font-size: 1.5rem; margin: 0;
        color: white !important; letter-spacing: 0.4px;
    }
    .main-header-left p { margin: 0.2rem 0 0; opacity: 0.82; font-size: 0.88rem; color: white; }

    /* ── Cards de módulo ── */
    .module-card {
        background: white;
        border: 2px solid #e2e6ea;
        border-radius: 14px;
        padding: 1.8rem 1.4rem;
        text-align: center;
        transition: all 0.2s ease;
        margin-bottom: 0.5rem;
    }
    .module-card:hover { border-color: #2c5f8a; box-shadow: 0 4px 18px rgba(44,95,138,.15); }
    .module-card .icon  { font-size: 2.4rem; margin-bottom: 0.6rem; }
    .module-card .title { font-family: 'Merriweather', serif; font-size: 1rem; font-weight: 700; color: #1a3a5c; }
    .module-card .desc  { font-size: 0.82rem; color: #6b7280; margin-top: 0.35rem; line-height: 1.4; }

    /* ── Cards de seção ── */
    .section-card {
        background: #f8f9fb;
        border: 1px solid #e2e6ea;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }
    .section-title {
        font-family: 'Merriweather', serif;
        font-size: 0.88rem; font-weight: 700;
        color: #1a3a5c; margin-bottom: 1rem;
        text-transform: uppercase; letter-spacing: 0.8px;
        border-bottom: 2px solid #2c5f8a; padding-bottom: 0.4rem;
    }

    /* ── Config panel ── */
    .config-panel {
        background: white;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 1.8rem;
        margin-bottom: 1.4rem;
        box-shadow: 0 2px 12px rgba(0,0,0,.06);
    }
    .config-group-title {
        font-family: 'Merriweather', serif;
        font-size: 0.82rem; font-weight: 700;
        color: #475569; margin: 1.4rem 0 0.8rem;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .config-group-title:first-child { margin-top: 0; }

    /* ── Botões primários ── */
    .stButton > button {
        background: linear-gradient(135deg, #1a3a5c, #2c5f8a) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 600 !important; font-size: 1rem !important;
        padding: 0.6rem 2rem !important; width: 100% !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }

    /* ── Log terminal ── */
    .log-box {
        background: #111827; color: #d1fae5;
        font-family: 'Courier New', monospace; font-size: 0.82rem;
        padding: 1rem 1.2rem; border-radius: 8px;
        max-height: 280px; overflow-y: auto;
        line-height: 1.6; white-space: pre-wrap; word-break: break-word;
    }

    /* ── Itens de proposição ── */
    .proposicao-item {
        background: white; border-left: 4px solid #2c5f8a;
        padding: 0.6rem 1rem; margin-bottom: 0.5rem;
        border-radius: 0 6px 6px 0; font-size: 0.88rem; color: #2d3748;
    }
    .badge     { display:inline-block; background:#ebf4ff; color:#2c5f8a; border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:600; margin-right:4px; }
    .badge-ep  { background:#fff7ed; color:#c2410c; }
    .badge-ok  { background:#f0fdf4; color:#166534; }

    /* ── Resultados ── */
    .success-box {
        background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px;
        padding:1rem 1.2rem; color:#166534; font-weight:600;
        text-align:center; margin-top:1rem;
    }
    .error-box {
        background:#fef2f2; border:1px solid #fecaca; border-radius:8px;
        padding:1rem 1.2rem; color:#991b1b; margin-top:1rem;
    }
    .info-saved {
        background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px;
        padding:0.8rem 1.2rem; color:#1e40af; font-weight:600;
        text-align:center; margin-top:0.8rem;
    }

    div[data-testid="stRadio"] > label { font-weight: 600; color: #374151; }
    
    /* ── Divider config ── */
    .config-divider {
        border: none; border-top: 1px solid #e2e8f0;
        margin: 1.2rem 0 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# Path dos módulos do projeto
# ──────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent
CONFIG_PATH  = PROJECT_ROOT / "configuracao.json"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT.parent / "proposicoes_bd"))

# ──────────────────────────────────────────────────────────
# Helpers de configuração
# ──────────────────────────────────────────────────────────
CONFIG_DEFAULTS = {
    "arquivo_modelo_conclusao":              "./modelos/modelo_conclusao.docx",
    "arquivo_modelo_conclusao_voto_separado":"./modelos/modelo_conclusao_voto_separado.docx",
    "arquivo_modelo_edital":                 "./modelos/modelo_edital.docx",
    "diretorio_geracao":                     "./arquivos_gerados/",
    "arquivo_planilha_de_projetos":          "./CONTROLE COFFFC 2026.xlsm",
    "planilha_de_projetos":                  "CONTROLE DE PL",
    "coluna_tipo_projeto":                   1,
    "coluna_ordem":                          2,
    "coluna_numero_projeto":                 3,
    "coluna_ementa":                         4,
    "coluna_parecer":                        7,
    "coluna_autor":                          5,
    "coluna_relatoria":                      6,
    "coluna_reuniao":                        9,
    "coluna_relatoria_vista":                14,
    "coluna_parecer_vista":                  15,
    "filtro_coluna_reuniao":                 "PRÓXIMA",
    "url_base":                              "http://alerjln1.alerj.rj.gov.br",
    "presidente_comissao":                   "ANDRÉ CORRÊA",
    "banco_dados_proposicoes":               "S:\\projetos_de_lei\\projetos_de_lei.accdb",
}

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Garante que chaves novas no default existam
        for k, v in CONFIG_DEFAULTS.items():
            data.setdefault(k, v)
        return data
    return dict(CONFIG_DEFAULTS)

def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)

# ──────────────────────────────────────────────────────────
# Captura de stdout → log visual em tempo real
# ──────────────────────────────────────────────────────────
class LogCapture(io.StringIO):
    def __init__(self, placeholder):
        super().__init__()
        self._placeholder = placeholder
        self._buffer = ""

    def write(self, text):
        self._buffer += text
        self._placeholder.markdown(
            f'<div class="log-box">{self._buffer}</div>',
            unsafe_allow_html=True,
        )
        return len(text)

    def flush(self):
        pass

# ──────────────────────────────────────────────────────────
# Estado de navegação
# ──────────────────────────────────────────────────────────
if "modulo"      not in st.session_state: st.session_state.modulo      = None
if "show_config" not in st.session_state: st.session_state.show_config = False

# ──────────────────────────────────────────────────────────
# Cabeçalho fixo com botão de engrenagem
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-header-left">
        <h1>⚖️ Sistema de Documentos · CCJ</h1>
        <p>Comissão de Constituição e Justiça · ALERJ</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Engrenagem como botão Streamlit (alinhado à direita via colunas)
col_space, col_gear = st.columns([5, 1])
with col_gear:
    gear_label = "✕ Fechar" if st.session_state.show_config else "⚙️ Config"
    if st.button(gear_label, key="btn_gear"):
        st.session_state.show_config = not st.session_state.show_config
        st.rerun()

# ──────────────────────────────────────────────────────────
# PAINEL DE CONFIGURAÇÕES (expansível)
# ──────────────────────────────────────────────────────────
if st.session_state.show_config:
    # Carrega o JSON uma única vez no session_state para não resetar os campos
    if "cfg" not in st.session_state:
        st.session_state.cfg = load_config()
    cfg = st.session_state.cfg

    # ── Helpers: abrem explorador do Windows via tkinter ──
    def browse_file(state_key: str, filetypes: list):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes("-topmost", True)
            path = filedialog.askopenfilename(filetypes=filetypes)
            root.destroy()
            if path:
                st.session_state.cfg[state_key] = path
        except Exception as e:
            st.warning(f"Não foi possível abrir o explorador: {e}")

    def browse_folder(state_key: str):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes("-topmost", True)
            path = filedialog.askdirectory()
            root.destroy()
            if path:
                st.session_state.cfg[state_key] = path + "/"
        except Exception as e:
            st.warning(f"Não foi possível abrir o explorador: {e}")

    def path_row(label: str, state_key: str, btn_key: str,
                 filetypes=None, is_folder=False, help=None):
        """Campo de texto + botão 📂 lado a lado."""
        col_input, col_btn = st.columns([8, 1])
        with col_input:
            val = st.text_input(label, value=st.session_state.cfg.get(state_key, ""),
                                key=f"ti_{state_key}", help=help)
            st.session_state.cfg[state_key] = val
        with col_btn:
            st.markdown("""
                <style>
                    div[data-testid="stButton"] button[kind="secondary"] {
                        padding: 0.4rem 0.6rem !important;
                        min-width: 2.2rem !important;
                        width: 100% !important;
                    }
                </style>
                <div style='margin-top:1.75rem;'>
            """, unsafe_allow_html=True)
            if st.button("📂", key=btn_key, help="Navegar…"):
                if is_folder:
                    browse_folder(state_key)
                else:
                    browse_file(state_key, filetypes or [("Todos os arquivos", "*.*")])
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    DOCX  = [("Word",   "*.docx"),        ("Todos", "*.*")]
    SHEET = [("Excel",  "*.xlsm *.xlsx"), ("Todos", "*.*")]
    DB    = [("Access", "*.accdb *.mdb"), ("Todos", "*.*")]

    st.markdown('<div class="config-panel">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Configurações do Sistema")
    st.caption("Digite o caminho ou clique em 📂 para navegar. As alterações são **salvas automaticamente** no `configuracao.json`.")

    # ── Arquivos e pastas ──
    st.markdown('<p class="config-group-title">📁 Arquivos e Pastas</p>', unsafe_allow_html=True)

    path_row("Planilha de projetos (.xlsm / .xlsx)", "arquivo_planilha_de_projetos", "br_planilha",
             filetypes=SHEET, help="Caminho completo ou relativo da planilha de controle.")
    path_row("Pasta de saída dos documentos", "diretorio_geracao", "br_dir",
             is_folder=True, help="Pasta onde os editais e conclusões serão salvos.")
    path_row("Modelo do Edital (.docx)",               "arquivo_modelo_edital",                  "br_edital",    filetypes=DOCX)
    path_row("Modelo de Conclusão (.docx)",            "arquivo_modelo_conclusao",               "br_conclusao", filetypes=DOCX)
    path_row("Modelo de Voto em Separado (.docx)",     "arquivo_modelo_conclusao_voto_separado", "br_voto",      filetypes=DOCX)
    path_row("Banco de dados (.accdb / .mdb)",         "banco_dados_proposicoes",                "br_banco",     filetypes=DB,
             help="Caminho para o banco Access com os links das proposições.")

    # ── Planilha ──
    st.markdown('<hr class="config-divider">', unsafe_allow_html=True)
    st.markdown('<p class="config-group-title">📊 Configurações da Planilha</p>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        cfg["planilha_de_projetos"] = st.text_input(
            "Nome da aba (sheet)",
            value=cfg["planilha_de_projetos"],
            key="cfg_aba",
        )
        cfg["filtro_coluna_reuniao"] = st.text_input(
            "Filtro da coluna Reunião",
            value=cfg["filtro_coluna_reuniao"],
            key="cfg_filtro",
            help="Valor que identifica os projetos da próxima reunião. Deixe vazio para sem filtro.",
        )
    with c4:
        cfg["presidente_comissao"] = st.text_input(
            "Presidente da Comissão",
            value=cfg["presidente_comissao"],
            key="cfg_presidente",
            help="Nome exatamente como aparece na planilha. Será o primeiro na ordenação.",
        )
        cfg["url_base"] = st.text_input(
            "URL base do site",
            value=cfg["url_base"],
            key="cfg_url",
        )

    st.markdown('<hr class="config-divider">', unsafe_allow_html=True)
    st.markdown('<p class="config-group-title">🔢 Número das Colunas na Planilha</p>', unsafe_allow_html=True)
    st.caption("Informe o número (1 = coluna A) de cada campo na planilha.")

    cc = st.columns(5)
    labels = [
        ("Tipo de projeto",   "coluna_tipo_projeto"),
        ("Ordem",             "coluna_ordem"),
        ("Número do projeto", "coluna_numero_projeto"),
        ("Ementa",            "coluna_ementa"),
        ("Autor(es)",         "coluna_autor"),
    ]
    for i, (lbl, key) in enumerate(labels):
        with cc[i]:
            cfg[key] = st.number_input(lbl, min_value=1, value=int(cfg[key]), step=1, key=f"col_{key}")

    cc2 = st.columns(5)
    labels2 = [
        ("Relator",           "coluna_relatoria"),
        ("Parecer",           "coluna_parecer"),
        ("Reunião",           "coluna_reuniao"),
        ("Relator Vista",     "coluna_relatoria_vista"),
        ("Parecer Vista",     "coluna_parecer_vista"),
    ]
    for i, (lbl, key) in enumerate(labels2):
        with cc2[i]:
            cfg[key] = st.number_input(lbl, min_value=1, value=int(cfg[key]), step=1, key=f"col_{key}")

    # Salva automaticamente a cada interação (qualquer mudança de campo dispara rerun)
    save_config(cfg)

    # ── Botão de confirmação visual ──
    st.markdown("")
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    with col_s2:
        if st.button("💾  Salvar e fechar", key="btn_save_cfg"):
            save_config(cfg)
            st.session_state.show_config = False
            st.session_state.pop("cfg", None)   # força releitura na próxima abertura
            st.rerun()

    st.markdown('<div class="info-saved">✅ Alterações salvas automaticamente no configuracao.json</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

# ──────────────────────────────────────────────────────────
# TELA INICIAL — escolha do módulo
# ──────────────────────────────────────────────────────────
if st.session_state.modulo is None:
    st.markdown("### O que deseja gerar hoje?")
    st.markdown("Escolha uma das funcionalidades abaixo para continuar.")
    st.markdown("")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="module-card">
            <div class="icon">📋</div>
            <div class="title">Edital de Pauta</div>
            <div class="desc">Gera o edital com a lista de proposições para a reunião, com ou sem hyperlinks e pareceres.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir Edital", key="btn_edital"):
            st.session_state.modulo = "edital"
            st.rerun()

    with col_b:
        st.markdown("""
        <div class="module-card">
            <div class="icon">📝</div>
            <div class="title">Conclusões</div>
            <div class="desc">Gera os documentos de conclusão para cada proposição da reunião, incluindo votos em separado.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir Conclusões", key="btn_conclusao"):
            st.session_state.modulo = "conclusao"
            st.rerun()

    st.stop()

# ──────────────────────────────────────────────────────────
# Breadcrumb / voltar
# ──────────────────────────────────────────────────────────
label_modulo = "📋 Edital de Pauta" if st.session_state.modulo == "edital" else "📝 Conclusões"
col_back, col_title = st.columns([1, 4])
with col_back:
    if st.button("← Voltar", key="btn_voltar"):
        st.session_state.modulo = None
        st.rerun()
with col_title:
    st.markdown(f"<h3 style='margin:0;padding-top:0.2rem;color:#1a3a5c;'>{label_modulo}</h3>", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════
# MÓDULO 1 — EDITAL
# ══════════════════════════════════════════════════════════
if st.session_state.modulo == "edital":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">⚙️ Parâmetros de Geração</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        numero_inicial = st.number_input(
            "Número inicial das proposições",
            min_value=1, value=1, step=1,
            help="A partir de qual número as proposições serão numeradas no edital.",
        )
    with col2:
        tipo = st.radio(
            "Tipo de saída",
            options=["link", "texto"],
            format_func=lambda x: "🔗 Com hyperlink" if x == "link" else "📝 Somente texto",
            horizontal=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        ordenacao = st.radio(
            "Ordenação",
            options=["comum", "nenhuma"],
            format_func=lambda x: "🔢 Padrão (por relator)" if x == "comum" else "🚫 Sem ordenação",
            horizontal=True,
        )
    with col4:
        inclui_parecer = st.checkbox("📄 Incluir pareceres", value=False)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Gerar Edital"):
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">🖥️ Log de Execução</p>', unsafe_allow_html=True)
        log_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

        arquivo_gerado = None
        proposicoes = []
        log_capture = LogCapture(log_placeholder)
        old_stdout = sys.stdout
        sys.stdout = log_capture

        try:
            from classes.aplicacao import Configuracao
            from classes.planilha import PlanilhaProjetos
            from classes.documento import Edital

            print("🔧 Carregando configurações...")
            config = Configuracao()

            print("\n📂 Carregando proposições da planilha...")
            P = PlanilhaProjetos(ordem_inicial=int(numero_inicial), ordenacao=ordenacao)
            proposicoes = P.CarregaColunas()
            print(f"✅ {len(proposicoes)} proposição(ões) carregada(s).\n")

            if not proposicoes:
                print("⚠️  Nenhuma proposição encontrada com os filtros atuais.")
            else:
                print("📋 Proposições selecionadas:")
                for d in proposicoes:
                    ep = " [EP]" if d.emenda_de_plenario else ""
                    print(f"   {d.ordem}. {d.numero}/{d.ano}{ep} — Relator: {d.relator or '(sem relator)'}")

                print("\n📝 Gerando documento...")
                edital = Edital(lista_proposicoes=proposicoes, inclui_parecer=inclui_parecer)
                edital.usar_link = (tipo == "link")

                dir_saida = Path(config.diretorio_geracao)
                edital.gera_documento(
                    arquivo_modelo=config.arquivo_modelo_edital,
                    diretorio_geracao=dir_saida,
                    banco_dados_proposicoes=config.banco_dados_proposicoes,
                )

                arquivos = sorted(dir_saida.glob("edital_*.docx"), key=lambda f: f.stat().st_mtime, reverse=True)
                if arquivos:
                    arquivo_gerado = arquivos[0]

                print("\n💾 Atualizando ordem na planilha...")
                resultado = P.AtualizaOrdemNosProjetos(proposicoes)
                print("✅ Planilha atualizada com sucesso." if resultado == "OK" else f"⚠️  {resultado}")

        except Exception as e:
            print(f"\n❌ Erro: {e}")
        finally:
            sys.stdout = old_stdout

        if arquivo_gerado and arquivo_gerado.exists():
            if proposicoes:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<p class="section-title">📄 Prévia das Proposições</p>', unsafe_allow_html=True)
                for p in proposicoes:
                    ep_badge = '<span class="badge badge-ep">EP</span>' if p.emenda_de_plenario else ''
                    rel = f'<span class="badge">{p.relator.title() if p.relator else "Sem relator"}</span>'
                    st.markdown(
                        f'<div class="proposicao-item">'
                        f'<strong>{p.ordem}.</strong> PL {p.numero}/{p.ano} {ep_badge} {rel}<br>'
                        f'<span style="color:#6b7280;font-size:0.83rem;">{p.ementa[:120]}{"…" if len(p.ementa)>120 else ""}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            with open(arquivo_gerado, "rb") as f:
                docx_bytes = f.read()

            st.markdown('<div class="success-box">✅ Edital gerado com sucesso! Clique abaixo para baixar.</div>', unsafe_allow_html=True)
            st.download_button(
                label=f"⬇️  Baixar {arquivo_gerado.name}",
                data=docx_bytes,
                file_name=arquivo_gerado.name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        elif "❌" in log_capture._buffer:
            st.markdown('<div class="error-box">❌ Ocorreu um erro durante a geração. Verifique o log acima.</div>', unsafe_allow_html=True)
        elif not proposicoes:
            st.warning("Nenhuma proposição foi encontrada. Verifique os filtros na planilha.")


# ══════════════════════════════════════════════════════════
# MÓDULO 2 — CONCLUSÕES
# ══════════════════════════════════════════════════════════
elif st.session_state.modulo == "conclusao":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">⚙️ Parâmetros da Sessão</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        data_sessao = st.date_input(
            "Data da sessão",
            value=datetime.today(),
            format="DD/MM/YYYY",
        )
    with col2:
        reuniao = st.text_input(
            "Identificação da reunião",
            placeholder="Ex: 1ª Reunião Ordinária de 2025",
        )

    st.markdown('</div>', unsafe_allow_html=True)

    pode_gerar = bool(reuniao and reuniao.strip())
    if not pode_gerar:
        st.info("ℹ️ Preencha a identificação da reunião para continuar.")

    if pode_gerar and st.button("🚀 Gerar Conclusões"):
        data_str = data_sessao.strftime("%d/%m/%Y")

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">🖥️ Log de Execução</p>', unsafe_allow_html=True)
        log_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

        proposicoes = []
        arquivos_gerados = []
        log_capture = LogCapture(log_placeholder)
        old_stdout = sys.stdout
        sys.stdout = log_capture

        try:
            from classes.aplicacao import Configuracao
            from classes.planilha import PlanilhaProjetos
            from classes.documento import proposicao_para_conclusao

            print("🔧 Carregando configurações...")
            config = Configuracao()

            print("\n📂 Carregando proposições da planilha...")
            P = PlanilhaProjetos()
            proposicoes = P.CarregaColunas()
            print(f"✅ {len(proposicoes)} proposição(ões) carregada(s).\n")

            if not proposicoes:
                print("⚠️  Nenhuma proposição encontrada com os filtros atuais.")
            else:
                dir_saida = Path(config.diretorio_geracao)
                mtime_antes = {f: f.stat().st_mtime for f in dir_saida.glob("Conclusao*.docx")}

                for proposicao in proposicoes:
                    ep = " [EP]" if proposicao.emenda_de_plenario else ""
                    print(f"📝 Gerando: {proposicao.numero}/{proposicao.ano}{ep} — {proposicao.relator or 'sem relator'}")
                    conclusao = proposicao_para_conclusao(proposicao)
                    conclusao.arquivo_modelo = config.arquivo_modelo_conclusao
                    conclusao.arquivo_modelo_voto_separado = config.arquivo_modelo_conclusao_vovo_separado
                    conclusao.diretorio_geracao = config.diretorio_geracao
                    conclusao.gera_documento(data_sessao=data_str, reuniao=reuniao.strip())

                arquivos_gerados = [
                    f for f in dir_saida.glob("Conclusao*.docx")
                    if f not in mtime_antes or f.stat().st_mtime != mtime_antes.get(f)
                ]
                arquivos_gerados.sort(key=lambda f: f.stat().st_mtime, reverse=True)
                print(f"\n✅ {len(arquivos_gerados)} arquivo(s) gerado(s) com sucesso.")

        except Exception as e:
            print(f"\n❌ Erro: {e}")
        finally:
            sys.stdout = old_stdout

        if arquivos_gerados:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">📄 Documentos Gerados</p>', unsafe_allow_html=True)
            for p in proposicoes:
                ep_badge = '<span class="badge badge-ep">EP</span>' if p.emenda_de_plenario else ''
                vs_badge = '<span class="badge" style="background:#fdf4ff;color:#7e22ce;">Voto Separado</span>' if p.parecer_vista else ''
                rel = f'<span class="badge">{p.relator.title() if p.relator else "Sem relator"}</span>'
                st.markdown(
                    f'<div class="proposicao-item">'
                    f'<span class="badge badge-ok">✓</span> PL {p.numero}/{p.ano} {ep_badge} {rel} {vs_badge}<br>'
                    f'<span style="color:#6b7280;font-size:0.83rem;">{p.ementa[:110]}{"…" if len(p.ementa)>110 else ""}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="success-box">✅ Conclusões geradas! Baixe os arquivos abaixo.</div>', unsafe_allow_html=True)
            st.markdown("")

            # ZIP com tudo
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for arq in arquivos_gerados:
                    zf.write(arq, arcname=arq.name)
            zip_buffer.seek(0)
            data_str_safe = data_sessao.strftime("%Y%m%d")
            st.download_button(
                label="📦  Baixar todas as conclusões (.zip)",
                data=zip_buffer.getvalue(),
                file_name=f"conclusoes_{data_str_safe}.zip",
                mime="application/zip",
                key="dl_zip",
            )

            st.markdown("<hr style='margin:0.8rem 0;border-color:#e2e6ea;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.85rem;color:#6b7280;margin-bottom:0.5rem;'>Ou baixe individualmente:</p>", unsafe_allow_html=True)

            for arq in arquivos_gerados:
                with open(arq, "rb") as f:
                    st.download_button(
                        label=f"⬇️  {arq.name}",
                        data=f.read(),
                        file_name=arq.name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_{arq.name}",
                    )

        elif "❌" in log_capture._buffer:
            st.markdown('<div class="error-box">❌ Ocorreu um erro durante a geração. Verifique o log acima.</div>', unsafe_allow_html=True)
        elif not proposicoes:
            st.warning("Nenhuma proposição foi encontrada. Verifique os filtros na planilha.")
