"""Pagina 3 - Interpretabilidade com SHAP."""
import streamlit as st
from pathlib import Path
from style import CORES

st.title("🔍 Interpretabilidade (SHAP)")
st.caption("Como o modelo decide — e por que a estatistica concorda com ele")

ROOT = Path(__file__).resolve().parents[2]  # pages -> app -> raiz
FIG  = ROOT / "reports" / "figures"

# ── Validação cruzada ────────────────────────────────────────────
st.markdown("""
<div class='card'>
<p>O SHAP abre a "caixa-preta" do XGBoost. O resultado mais forte e a
<strong>convergencia entre tres metodos independentes</strong>: o tamanho de
efeito (Mann-Whitney, na EDA), a importancia global SHAP e os casos individuais
— todos apontam <strong>V14 &gt; V4 &gt; V12</strong> como as variaveis mais
discriminativas. Isso e robustez real, nao artefato do modelo.</p>
</div>
""", unsafe_allow_html=True)

# ── Importância global ───────────────────────────────────────────
st.subheader("Importancia global das features")
fig_sum = FIG / "nb05_shap_summary.png"
if fig_sum.exists():
    st.image(str(fig_sum), use_container_width=True)
    st.caption("Beeswarm SHAP — vermelho = valor alto da feature. "
               "V14, V4 e V12 dominam, confirmando a EDA.")

# ── Casos individuais ────────────────────────────────────────────
st.subheader("Anatomia de duas decisoes")
st.markdown("""
O par abaixo explica o **teto de recall (~80%)** do modelo: ele acerta as
fraudes de assinatura extrema, mas nao detecta as camufladas.
""")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Fraude DETECTADA** (P=1,000)")
    fig_tp = FIG / "nb05_waterfall_tp.png"
    if fig_tp.exists():
        st.image(str(fig_tp), use_container_width=True)
    st.markdown("""
    <div class='card'>
    <p>V14=-13,7 e V12=-13,1 — valores <strong>extremos</strong>, longe do
    padrao legitimo (~0). Assinatura caricatural: o modelo decide com certeza.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("**Fraude que ESCAPOU** (P=0,000)")
    fig_fn = FIG / "nb05_waterfall_fn.png"
    if fig_fn.exists():
        st.image(str(fig_fn), use_container_width=True)
    st.markdown("""
    <div class='card'>
    <p>V14=-0,01, V4=0,90 — valores <strong>proximos do normal</strong>. Fraude
    camuflada que imita uma transacao legitima. Sem sinal detectavel.</p>
    </div>
    """, unsafe_allow_html=True)

st.info("Licao: os ~20% de fraudes que escapam sao um **limite estrutural** do "
        "problema (fraudes desenhadas para parecer legitimas), nao falha de ajuste.")
