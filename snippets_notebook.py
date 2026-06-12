# ════════════════════════════════════════════════════════════════
# SNIPPETS PADRÃO DE NOTEBOOK — copiar conforme necessário
# ════════════════════════════════════════════════════════════════
# Estes blocos resolvem dores recorrentes:
#  1. Setup repetido no topo de todo notebook
#  2. O bug clássico do `df` virar 'method' (df = df.head sem parênteses)
#     que estoura "TypeError: 'method' object is not subscriptable"
# ════════════════════════════════════════════════════════════════


# ────────────────────────────────────────────────────────────────
# SNIPPET 1 — Cabeçalho de setup (1ª célula de qualquer notebook)
# ────────────────────────────────────────────────────────────────
"""
# ════════════════════════════════════════════════════════════════
# NB0X — <TÍTULO> | <PROJETO>
# Célula 1 — Setup
# ════════════════════════════════════════════════════════════════
%load_ext autoreload
%autoreload 2

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from src.config     import CONFIG, CAMINHOS
from src.viz_config import PALETTE, CORES   # aplica tema dark no import

# ── Caminhos e constantes ────────────────────────────────────────
DADOS_BRUTOS = CAMINHOS.dados_raw / CAMINHOS.dados_brutos
DADOS_PRO    = CAMINHOS.dados_processed
MODELS_DIR   = CAMINHOS.modelos
FIGURAS_DIR  = CAMINHOS.figures
REPORTS_DIR  = CAMINHOS.reports
RANDOM_STATE = CONFIG["dados"]["random_state"]

for d in (DADOS_PRO, MODELS_DIR, FIGURAS_DIR):
    d.mkdir(parents=True, exist_ok=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)

print("✅ Setup configurado")
print(f"   SEED: {RANDOM_STATE}")
"""


# ────────────────────────────────────────────────────────────────
# SNIPPET 2 — Padrão df_bruto / df.copy() (carregamento robusto)
# ────────────────────────────────────────────────────────────────
# Carregue SEMPRE em df_bruto (imutável) e trabalhe numa cópia.
# Se algo corromper o df, recomeçar = df = df_bruto.copy() (sem reler).
"""
df_bruto = pd.read_parquet(DADOS_PRO / "dados.parquet")   # ou read_csv/read_excel
df       = df_bruto.copy()
print(f"✅ Carregado: {len(df_bruto):,} linhas × {df_bruto.shape[1]} colunas")
"""


# ────────────────────────────────────────────────────────────────
# SNIPPET 3 — Proteção do df (1ª linha de células de limpeza)
# ────────────────────────────────────────────────────────────────
# Torna a célula idempotente: sempre parte do bruto, não importa o
# estado do df. Mata o bug do "df virou method" de uma vez.
"""
df = df_bruto.copy()   # idempotente: pode rodar quantas vezes quiser
"""

# Variante defensiva (quando você só tem o df, não o df_bruto):
"""
if not isinstance(df, pd.DataFrame):
    print("⚠️  df não era DataFrame — reconstruindo")
    df = pd.concat(abas.values(), ignore_index=True)   # ajuste à sua fonte
"""


# ────────────────────────────────────────────────────────────────
# SNIPPET 4 — Bloco de fechamento de notebook (resumo)
# ────────────────────────────────────────────────────────────────
"""
print('''
╔══════════════════════════════════════════════════════════════╗
║              RESUMO DO NB0X — <TÍTULO>                        ║
╚══════════════════════════════════════════════════════════════╝

<O QUE FOI FEITO>
  • ...

ARTEFATOS
  • ...

PRÓXIMO PASSO → NB0X+1 (<TÍTULO>)
  • ...
''')
"""
