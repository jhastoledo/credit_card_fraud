"""Pagina 4 - Classificador ao vivo (exemplos do dataset + upload de CSV)."""
import streamlit as st
import pandas as pd
from pathlib import Path
from utils import carregar_pipeline, carregar_json, df_para_csv_bytes
from style import CORES

st.title("💳 Classificador de Transacoes")
st.caption("Teste o modelo: escolha um exemplo ou envie suas transacoes")

# ── Carregar pipeline e threshold ────────────────────────────────
pipeline  = carregar_pipeline("pipeline_final.joblib")
meta      = carregar_json("metadados.json")
THRESHOLD = meta["threshold"]

ROOT = Path(__file__).resolve().parents[2]  # pages -> app -> raiz
EXEMPLOS_CSV = ROOT / "app" / "exemplos.csv"

# Colunas que o modelo espera (o pipeline descarta Time internamente)
COLS_ESPERADAS = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]


def classificar(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Aplica o pipeline + threshold. Retorna df com predicao e probabilidade."""
    proba = pipeline.predict_proba(df_raw[COLS_ESPERADAS])[:, 1]
    pred  = (proba >= THRESHOLD).astype(int)
    out = pd.DataFrame({
        "P(fraude)": proba.round(4),
        "Classificacao": ["🚨 FRAUDE" if p == 1 else "✅ Legitima" for p in pred],
    })
    return out


def mostrar_resultado(df_raw, resultado, gabarito=None):
    """Renderiza o resultado da classificacao."""
    for i in range(len(resultado)):
        proba = resultado.iloc[i]["P(fraude)"]
        classe = resultado.iloc[i]["Classificacao"]
        cor = CORES["vermelho"] if "FRAUDE" in classe else CORES["verde"]
        extra = ""
        if gabarito is not None:
            real = "FRAUDE" if gabarito.iloc[i] == 1 else "Legitima"
            acertou = ("FRAUDE" in classe) == (gabarito.iloc[i] == 1)
            extra = (f" · Real: <strong>{real}</strong> "
                     f"{'✔️ acertou' if acertou else '❌ errou'}")
        st.markdown(f"""
        <div class='card' style='border-left-color:{cor}'>
        <p style='font-size:1.1em'><strong>{classe}</strong> ·
        P(fraude) = <strong>{proba:.4f}</strong> (threshold {THRESHOLD:.3f}){extra}</p>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# MODO 1 — Exemplos do dataset
# ════════════════════════════════════════════════════════════════
st.subheader("Modo 1 · Exemplos do dataset")
st.markdown("Transacoes reais do conjunto de teste (com gabarito para conferir).")

if EXEMPLOS_CSV.exists():
    exemplos = pd.read_csv(EXEMPLOS_CSV)
    gabarito_col = exemplos["Class"] if "Class" in exemplos.columns else None
    exemplos_X = exemplos.drop(columns=["Class"]) if "Class" in exemplos.columns else exemplos

    # Rótulos amigáveis para o seletor
    rotulos = []
    for i in range(len(exemplos_X)):
        amount = exemplos_X.iloc[i]["Amount"]
        real = ""
        if gabarito_col is not None:
            real = " (fraude real)" if gabarito_col.iloc[i] == 1 else " (legitima real)"
        rotulos.append(f"Exemplo {i+1} · £{amount:.2f}{real}")

    escolha = st.selectbox("Escolha uma transacao:", range(len(rotulos)),
                           format_func=lambda i: rotulos[i])

    if st.button("Classificar exemplo", type="primary"):
        linha = exemplos_X.iloc[[escolha]]
        resultado = classificar(linha)
        gab = gabarito_col.iloc[[escolha]] if gabarito_col is not None else None
        mostrar_resultado(linha, resultado, gab)
else:
    st.warning("Arquivo de exemplos nao encontrado (app/exemplos.csv).")

# ════════════════════════════════════════════════════════════════
# MODO 2 — Upload de CSV
# ════════════════════════════════════════════════════════════════
st.divider()
st.subheader("Modo 2 · Enviar transacoes (CSV)")
st.markdown(f"""
Envie um CSV com as colunas: `Time`, `V1`...`V28`, `Amount`.
O modelo classifica em lote. (A coluna `Class`, se presente, e usada como gabarito.)
""")

upload = st.file_uploader("Arquivo CSV", type=["csv"])
if upload is not None:
    try:
        df_up = pd.read_csv(upload)
        faltando = [c for c in COLS_ESPERADAS if c not in df_up.columns]
        if faltando:
            st.error(f"Colunas faltando no CSV: {faltando}")
        else:
            resultado = classificar(df_up)
            n_fraude = (resultado["Classificacao"].str.contains("FRAUDE")).sum()
            st.success(f"Classificadas {len(resultado)} transacoes · "
                       f"{n_fraude} fraude(s) detectada(s)")

            # Juntar resultado ao df para exibição
            df_final = pd.concat([resultado, df_up[["Amount"]].reset_index(drop=True)], axis=1)
            st.dataframe(df_final, use_container_width=True)

            # Download dos resultados
            st.download_button(
                "Baixar resultados (CSV)",
                df_para_csv_bytes(df_final, index=False),
                "resultados_classificacao.csv",
                "text/csv",
            )
    except Exception as e:
        st.error(f"Erro ao processar o CSV: {e}")
