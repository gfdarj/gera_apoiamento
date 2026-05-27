import streamlit as st
import sys
import os
import io
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────
# Configuração de página
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gerador de Edital",
    page_icon="📋",
    layout="centered",
)

# ──────────────────────────────────────────────────────────
# CSS customizado
# ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Merriweather', serif !important;
    }

    .main-header {
        background: linear-gradient(135deg, #1a3a5c 0%, #2c5f8a 100%);
        padding: 2rem 2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }

    .main-header h1 {
        font-size: 1.8rem;
        margin: 0;
        color: white !important;
        letter-spacing: 0.5px;
    }

    .main-header p {
        margin: 0.5rem 0 0;
        opacity: 0.85;
        font-size: 0.95rem;
    }

    .section-card {
        background: #f8f9fb;
        border: 1px solid #e2e6ea;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
    }

    .section-title {
        font-family: 'Merriweather', serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #1a3a5c;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        border-bottom: 2px solid #2c5f8a;
        padding-bottom: 0.4rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1a3a5c, #2c5f8a) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.6rem 2rem !important;
        width: 100% !important;
        transition: opacity 0.2s !important;
    }

    .stButton > button:hover {
        opacity: 0.88 !important;
    }

    .log-box {
        background: #111827;
        color: #d1fae5;
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        max-height: 280px;
        overflow-y: auto;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
    }

    .proposicao-item {
        background: white;
        border-left: 4px solid #2c5f8a;
        padding: 0.6rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.88rem;
        color: #2d3748;
    }

    .badge {
        display: inline-block;
        background: #ebf4ff;
        color: #2c5f8a;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 4px;
    }

    .badge-ep {
        background: #fff7ed;
        color: #c2410c;
    }

    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #166534;
        font-weight: 600;
        text-align: center;
        margin-top: 1rem;
    }

    .error-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #991b1b;
        margin-top: 1rem;
    }

    div[data-testid="stRadio"] > label {
        font-weight: 600;
        color: #374151;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# Ajuste de path para encontrar os módulos do projeto
# ──────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT.parent / "proposicoes_bd"))

# ──────────────────────────────────────────────────────────
# Captura de stdout para exibir log em tempo real
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
# Cabeçalho
# ──────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📋 Gerador de Edital</h1>
    <p>Departamento de Apoio às Comissões Permanentes · ALERJ</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# Formulário de parâmetros
# ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">⚙️ Parâmetros de Geração</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    numero_inicial = st.number_input(
        "Número inicial das proposições",
        min_value=1,
        value=1,
        step=1,
        help="A partir de qual número as proposições serão numeradas no edital.",
    )

with col2:
    tipo = st.radio(
        "Tipo de saída",
        options=["link", "texto"],
        format_func=lambda x: "🔗 Com hyperlink" if x == "link" else "📝 Somente texto",
        horizontal=True,
        help="Define se o nome do projeto virará um link clicável no documento.",
    )

col3, col4 = st.columns(2)

with col3:
    ordenacao = st.radio(
        "Ordenação",
        options=["comum", "nenhuma"],
        format_func=lambda x: "🔢 Padrão (por relator)" if x == "comum" else "🚫 Sem ordenação",
        horizontal=True,
        help="'Padrão' agrupa por relator com o presidente da comissão primeiro.",
    )

with col4:
    inclui_parecer = st.checkbox(
        "📄 Incluir pareceres",
        value=False,
        help="Adiciona o parecer e eventuais votos em separado a cada proposição.",
    )

st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
# Botão de geração
# ──────────────────────────────────────────────────────────
gerar = st.button("🚀 Gerar Edital")

if gerar:
    # Área de log
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">🖥️ Log de Execução</p>', unsafe_allow_html=True)
    log_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

    arquivo_gerado = None

    # Redireciona print() para o log visual
    log_capture = LogCapture(log_placeholder)
    old_stdout = sys.stdout
    sys.stdout = log_capture

    try:
        from classes.aplicacao import Configuracao
        from classes.planilha import PlanilhaProjetos
        from classes.documento import Edital

        print("🔧 Carregando configurações...")
        config = Configuracao()

        print(f"\n📂 Carregando proposições da planilha...")
        P = PlanilhaProjetos(
            ordem_inicial=int(numero_inicial),
            ordenacao=ordenacao,
        )
        proposicoes = P.CarregaColunas()
        print(f"✅ {len(proposicoes)} proposição(ões) carregada(s).\n")

        if len(proposicoes) == 0:
            print("⚠️  Nenhuma proposição encontrada com os filtros atuais.")
        else:
            print("📋 Proposições selecionadas:")
            for d in proposicoes:
                ep = " [EP]" if d.emenda_de_plenario else ""
                print(f"   {d.ordem}. {d.numero}/{d.ano}{ep} — Relator: {d.relator or '(sem relator)'}")

            print("\n📝 Gerando documento...")
            edital = Edital(
                lista_proposicoes=proposicoes,
                inclui_parecer=inclui_parecer,
            )
            edital.usar_link = (tipo == "link")

            # Diretório temporário para download
            dir_saida = Path(config.diretorio_geracao)
            edital.gera_documento(
                arquivo_modelo=config.arquivo_modelo_edital,
                diretorio_geracao=dir_saida,
                banco_dados_proposicoes=config.banco_dados_proposicoes,
            )

            # Encontra o arquivo mais recente gerado
            arquivos = sorted(
                dir_saida.glob("edital_*.docx"),
                key=lambda f: f.stat().st_mtime,
                reverse=True,
            )
            if arquivos:
                arquivo_gerado = arquivos[0]

            print("\n💾 Atualizando ordem na planilha...")
            resultado = P.AtualizaOrdemNosProjetos(proposicoes)
            if resultado == "OK":
                print("✅ Planilha atualizada com sucesso.")
            else:
                print(f"⚠️  {resultado}")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        sys.stdout = old_stdout

    # ──────────────────────────────────────────────────────
    # Resultado: prévia + download
    # ──────────────────────────────────────────────────────
    if arquivo_gerado and arquivo_gerado.exists():

        # Prévia das proposições
        if 'proposicoes' in dir() and proposicoes:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">📄 Prévia das Proposições</p>', unsafe_allow_html=True)
            for p in proposicoes:
                ep_badge = '<span class="badge badge-ep">EP</span>' if p.emenda_de_plenario else ''
                relator_info = f'<span class="badge">{p.relator.title() if p.relator else "Sem relator"}</span>'
                st.markdown(
                    f'<div class="proposicao-item">'
                    f'<strong>{p.ordem}.</strong> PL {p.numero}/{p.ano} {ep_badge} {relator_info}<br>'
                    f'<span style="color:#6b7280; font-size:0.83rem;">{p.ementa[:120]}{"…" if len(p.ementa) > 120 else ""}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

        # Botão de download
        with open(arquivo_gerado, "rb") as f:
            docx_bytes = f.read()

        st.markdown(
            '<div class="success-box">✅ Edital gerado com sucesso! Clique abaixo para baixar.</div>',
            unsafe_allow_html=True,
        )
        st.download_button(
            label=f"⬇️  Baixar {arquivo_gerado.name}",
            data=docx_bytes,
            file_name=arquivo_gerado.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    else:
        # Verifica se houve erro nos logs
        if "❌" in log_capture._buffer:
            st.markdown(
                '<div class="error-box">❌ Ocorreu um erro durante a geração. Verifique o log acima.</div>',
                unsafe_allow_html=True,
            )
        elif "⚠️" in log_capture._buffer and "Nenhuma proposição" in log_capture._buffer:
            st.warning("Nenhuma proposição foi encontrada. Verifique os filtros na planilha.")

