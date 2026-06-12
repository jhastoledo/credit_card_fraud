"""Pagina 1 - Visao Geral do problema de deteccao de fraude."""
import streamlit as st
from style import CORES

st.title("💳 Deteccao de Fraude em Cartao de Credito")
st.caption("Classificacao sob desbalanceamento extremo (578:1) · XGBoost + SHAP")

# ── Contexto ─────────────────────────────────────────────────────
st.markdown("""
<div class='card'>
<p>Este projeto detecta <strong>transacoes fraudulentas</strong> em um conjunto
de <strong>284.807 transacoes</strong> de cartao de credito (dataset ULB/Kaggle).
O desafio central e o <strong>desbalanceamento extremo</strong>: apenas
<strong>0,17%</strong> das transacoes sao fraude — uma razao de 578 transacoes
legitimas para cada fraude.</p>
</div>
""", unsafe_allow_html=True)

# ── Métricas do dataset ──────────────────────────────────────────
st.subheader("O dataset")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transacoes", "284.807")
col2.metric("Fraudes", "473", "0,167%")
col3.metric("Desbalanceamento", "578:1")
col4.metric("Features", "30")

st.markdown("""
<div class='card'>
<p><strong>Por que e dificil?</strong> Com 578:1, um modelo que classifica
<em>tudo como legitimo</em> acerta 99,83% das vezes — e e completamente inutil.
Por isso a metrica usada nao e a acuracia, e sim o <strong>PR-AUC</strong>
(Precision-Recall AUC), sensivel ao desempenho na classe rara.</p>
</div>
""", unsafe_allow_html=True)

# ── Features ─────────────────────────────────────────────────────
st.subheader("As variaveis")
st.markdown("""
- **`V1` a `V28`** — componentes de **PCA anonimizados** por privacidade.
  Nao tem significado semantico divulgado, mas carregam quase todo o sinal
  discriminativo (a EDA mostrou que `V14`, `V4` e `V12` separam fraude de
  legitima com tamanho de efeito ~0,9).
- **`Amount`** — valor da transacao. Fraudes tendem a valores baixos (mediana
  de £9 contra £22 das legitimas — padrao de "teste de cartao").
- **`Time`** — segundos desde a primeira transacao. Descartado por ser um valor
  absoluto que nao generaliza.
""")

# ── Abordagem ────────────────────────────────────────────────────
st.subheader("A abordagem")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    **Pipeline analitico (6 notebooks)**
    1. EDA estatistica (Mann-Whitney, normalidade)
    2. Feature engineering (RobustScaler, split estratificado)
    3. Comparacao de 7 modelos (PR-AUC)
    4. Tuning com Optuna (40 trials)
    5. Interpretabilidade (SHAP)
    6. Relatorio final
    """)
with col_b:
    st.markdown("""
    **Resultado final**
    - Modelo: **XGBoost** afinado
    - PR-AUC (teste): **0,826**
    - Recall: **81%** (77 de 95 fraudes)
    - Precision: **95%** (so 4 falsos alarmes)
    - Threshold: **0,264** (otimizado para F1)
    """)

st.info("Navegue pelas paginas: **Modelo** (desempenho), "
        "**Interpretabilidade** (SHAP) e **Classificador** (teste ao vivo).")
