"""
main.py - App de Deteccao de Fraude em Cartao de Credito.
Entry point com navegacao entre 4 paginas + rodape do autor na sidebar.

Rodar:  streamlit run app/main.py
"""
import streamlit as st
from style import aplicar_estilo, CORES

st.set_page_config(
    page_title="Deteccao de Fraude",
    page_icon="💳",
    layout="wide",
)
aplicar_estilo()

# ── Navegacao entre paginas (arquivos em app/pages/) ────────────
paginas = [
    st.Page("pages/1_visao_geral.py",   title="Visao Geral",        icon="📊"),
    st.Page("pages/2_modelo.py",        title="Modelo",             icon="🎯"),
    st.Page("pages/3_shap.py",          title="Interpretabilidade", icon="🔍"),
    st.Page("pages/4_classificador.py", title="Classificador",      icon="💳"),
]
nav = st.navigation(paginas)

# ── Rodape do autor na sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='
        margin-top: 2rem;
        padding: 1rem;
        background: {CORES["surf"]};
        border: 1px solid {CORES["borda"]};
        border-radius: 10px;
        text-align: center;
    '>
      <div style='
          font-size: 1.05em;
          font-weight: 600;
          color: {CORES["azul"]};
          margin-bottom: 0.1rem;
      '>Jhonnes Toledo</div>
      <div style='
          font-size: 0.8em;
          color: {CORES["texto2"]};
          margin-bottom: 0.7rem;
      '>Data Science</div>
      <div style='display: flex; gap: 0.5rem; justify-content: center;'>
        <a href='https://www.linkedin.com/in/jhostoledo' target='_blank'
           style='
              display: inline-flex; align-items: center; gap: 4px;
              padding: 5px 11px;
              background: #0077b5; color: white;
              border-radius: 6px; text-decoration: none;
              font-size: 0.8em; font-weight: 500;
           '>in LinkedIn</a>
        <a href='https://github.com/jhastoledo' target='_blank'
           style='
              display: inline-flex; align-items: center; gap: 4px;
              padding: 5px 11px;
              background: {CORES["borda"]}; color: {CORES["texto"]};
              border-radius: 6px; text-decoration: none;
              font-size: 0.8em; font-weight: 500;
           '>GitHub</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

nav.run()
