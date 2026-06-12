"""
utils.py — Carregamento de artefatos do app Streamlit (template).
Padrões deploy-safe validados em projetos anteriores:
  • Resolução de path relativa ao arquivo (funciona no Streamlit Cloud)
  • @st.cache_resource para objetos pesados (pipeline)
  • @st.cache_data para dados (parquets, json)

Ajuste os nomes de arquivo conforme o projeto.
"""
from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st

# ── Raiz do projeto: app/utils.py → sobe 2 níveis (deploy-safe) ──
# NUNCA use caminhos absolutos nem os.getcwd() — quebram no Cloud.
ROOT       = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"
DADOS_PRO  = ROOT / "data" / "processed"


# ── Carregamento com cache ───────────────────────────────────────
@st.cache_resource
def carregar_pipeline(nome: str = "pipeline_final.joblib"):
    """Pipeline final treinado. cache_resource = objeto pesado, 1 instância."""
    return joblib.load(MODELS_DIR / nome)


@st.cache_data
def carregar_json(nome: str):
    """Carrega um .json de models/ (ex.: personas.json, metadados)."""
    with open(MODELS_DIR / nome, encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def carregar_parquet(nome: str = "features.parquet"):
    """Carrega um .parquet de data/processed/. cache_data = dados serializáveis."""
    return pd.read_parquet(DADOS_PRO / nome)


# ── Helper de download de CSV (para resultados/exemplos) ─────────
@st.cache_data
def df_para_csv_bytes(df: pd.DataFrame, index: bool = True) -> bytes:
    """Converte DataFrame em bytes UTF-8 para st.download_button."""
    return df.to_csv(index=index).encode("utf-8")


# ── Inferência genérica (pipeline aplica todo o pré-processamento)
def prever(df_raw: pd.DataFrame, pipeline, cols: list[str]):
    """
    Aplica o pipeline a dados CRUS (o pré-processamento vive no pipeline).
    Retorna o array de predições. Ajuste para predict_proba se necessário.
    """
    return pipeline.predict(df_raw[cols])
