"""Pagina 2 - Desempenho do modelo."""
import streamlit as st
from pathlib import Path
from utils import carregar_json
from style import CORES

st.title("🎯 Desempenho do Modelo")
st.caption("XGBoost afinado via Optuna · avaliado no conjunto de teste intocado")

# ── Carregar métricas ────────────────────────────────────────────
meta = carregar_json("metadados.json")
ROOT = Path(__file__).resolve().parents[2]  # pages -> app -> raiz
FIG  = ROOT / "reports" / "figures"

# ── Métricas principais ──────────────────────────────────────────
st.subheader("Metricas no teste")
c1, c2, c3, c4 = st.columns(4)
c1.metric("PR-AUC", f"{meta['pr_auc_teste']:.3f}", "metrica primaria")
c2.metric("Recall", f"{meta['recall_teste']:.3f}", "fraudes detectadas")
c3.metric("Precision", f"{meta['precision_teste']:.3f}", "acerto dos alertas")
c4.metric("F1", f"{meta['f1_teste']:.3f}")

st.markdown(f"""
<div class='card'>
<p>O modelo opera no <strong>threshold {meta['threshold']:.3f}</strong>
(otimizado para maximo F1, abaixo do padrao 0,5 para capturar mais fraudes).
No teste de <strong>56.746 transacoes</strong> com 95 fraudes reais, detecta
<strong>77 fraudes</strong> gerando apenas <strong>4 falsos alarmes</strong>.</p>
</div>
""", unsafe_allow_html=True)

# ── PR-AUC vs ROC-AUC ────────────────────────────────────────────
st.subheader("Por que PR-AUC e nao ROC-AUC?")
col1, col2 = st.columns(2)
col1.metric("ROC-AUC (teste)", f"{meta['roc_auc_teste']:.3f}", "enganoso aqui")
col2.metric("PR-AUC (teste)", f"{meta['pr_auc_teste']:.3f}", "metrica honesta")
st.markdown("""
<div class='card'>
<p>Com desbalanceamento de 578:1, o <strong>ROC-AUC fica enganosamente alto</strong>
(0,974) mesmo para modelos medianos, pois a classe majoritaria domina a curva.
O <strong>PR-AUC</strong> e sensivel ao desempenho real na classe rara — por isso
foi a metrica que guiou todas as decisoes do projeto.</p>
</div>
""", unsafe_allow_html=True)

# ── Avaliação visual ─────────────────────────────────────────────
st.subheader("Avaliacao no teste")
fig_aval = FIG / "nb04_avaliacao.png"
if fig_aval.exists():
    st.image(str(fig_aval), use_container_width=True)
    st.caption("Matriz de confusao + curvas Precision-Recall e ROC")

# ── Comparação de modelos ────────────────────────────────────────
st.subheader("Comparacao de modelos")
fig_comp = FIG / "nb03_comparativo_modelos.png"
if fig_comp.exists():
    st.image(str(fig_comp), use_container_width=True)
    st.caption("7 modelos comparados por PR-AUC (5-fold StratifiedKFold)")

# ── Tuning ───────────────────────────────────────────────────────
st.subheader("Tuning com Optuna")
fig_opt = FIG / "nb04_optuna.png"
if fig_opt.exists():
    st.image(str(fig_opt), use_container_width=True)
    st.caption("40 trials · XGBoost vs RandomForest na mesma busca")

# ── Hiperparâmetros ──────────────────────────────────────────────
with st.expander("Hiperparametros do modelo final"):
    hp = meta["hiperparametros"]
    st.json(hp)
