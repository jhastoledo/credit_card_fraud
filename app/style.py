"""
style.py — Tema visual do app Streamlit (GitHub Dark).
Template reutilizável: espelha as cores do src/viz_config dos notebooks,
garantindo consistência visual entre notebooks, relatório HTML e app.

Uso no main.py:
    from style import aplicar_estilo
    aplicar_estilo()

Uso nas páginas:
    from style import CORES, PALETTE
"""
import streamlit as st

# ── Paleta GitHub Dark (idêntica ao viz_config dos notebooks) ────
CORES = {
    "fundo":    "#0d1117",
    "surf":     "#161b22",
    "borda":    "#30363d",
    "texto":    "#e6edf3",
    "texto2":   "#8b949e",
    "azul":     "#58a6ff",
    "verde":    "#3fb950",
    "roxo":     "#d2a8ff",
    "laranja":  "#ffa657",
    "vermelho": "#ff7b72",
    "amarelo":  "#e3b341",
}

# Paleta por categoria/cluster (mesma ordem dos notebooks)
PALETTE = ["#58a6ff", "#ff7b72", "#3fb950", "#d2a8ff", "#ffa657", "#79c0ff"]


def aplicar_estilo():
    """Injeta CSS global com o tema dark. Chamar uma vez no main.py."""
    c = CORES
    st.markdown(f"""
    <style>
      .stApp {{ background: {c['fundo']}; color: {c['texto']}; }}
      h1, h2, h3 {{ color: {c['azul']}; }}
      [data-testid="stSidebar"] {{
        background: {c['surf']};
        border-right: 1px solid {c['borda']};
      }}
      [data-testid="stMetricValue"] {{ color: {c['verde']}; }}
      div[data-testid="stMetric"] {{
        background: {c['surf']};
        border: 1px solid {c['borda']};
        border-radius: 8px;
        padding: 12px 16px;
      }}
      .stDataFrame {{ border: 1px solid {c['borda']}; border-radius: 8px; }}
      /* Card genérico (use via st.markdown com unsafe_allow_html=True) */
      .card {{
        background: {c['surf']};
        border: 1px solid {c['borda']};
        border-left: 4px solid {c['azul']};
        border-radius: 8px;
        padding: 16px 20px;
        margin: 10px 0;
      }}
      .acao-box {{
        background: {c['fundo']};
        border: 1px dashed {c['borda']};
        border-radius: 6px;
        padding: 10px 14px;
        margin-top: 10px;
        color: {c['laranja']};
        font-size: 0.95em;
      }}
    </style>
    """, unsafe_allow_html=True)


# Helper opcional: layout padrão de gráfico Plotly com o tema dark
def layout_plotly(fig, height=400):
    """Aplica o tema dark a uma figura Plotly. Retorna a própria fig."""
    fig.update_layout(
        plot_bgcolor=CORES["surf"],
        paper_bgcolor=CORES["fundo"],
        font_color=CORES["texto"],
        height=height,
    )
    fig.update_xaxes(gridcolor=CORES["borda"])
    fig.update_yaxes(gridcolor=CORES["borda"])
    return fig
