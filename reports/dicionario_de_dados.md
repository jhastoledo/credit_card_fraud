# 📖 Dicionário de Dados — Credit Card Fraud

Dataset real de transações de cartão de crédito de portadores europeus,
coletado em setembro de 2013 pela ULB (Université Libre de Bruxelles) —
benchmark clássico para detecção de fraude sob desbalanceamento extremo.

**Fonte:** [Credit Card Fraud Detection — Kaggle (ULB)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
**Arquivo:** `creditcard.csv` (compactado como `creditcard.zip`)
**Transações:** 284.807 (após remoção de duplicatas: 283.726)
**Colunas:** 31 (Time + V1–V28 + Amount + Class)
**Período:** 2 dias de setembro de 2013
**Nota:** 28 das 30 features são componentes PCA anonimizados por privacidade.

---

## Features Originais

### Target

| Coluna | Tipo | Descrição | Valores |
|---|---|---|---|
| `Class` | int | **Target** — transação fraudulenta | 0 = legítima, 1 = fraude |

> Taxa de fraude: 0,167% (473 de 283.726 após limpeza). Desbalanceamento 578:1.

### Features Não-Anonimizadas

| Coluna | Tipo | Descrição | Observações |
|---|---|---|---|
| `Time` | float | Segundos decorridos desde a primeira transação | Valor absoluto — **descartado** (não generaliza) |
| `Amount` | float | Valor da transação | Assimétrico, cauda longa (até £25.691) |

### Features Anonimizadas (PCA)

| Coluna | Tipo | Descrição |
|---|---|---|
| `V1` – `V28` | float | Componentes principais (PCA) das features originais |

> As 28 componentes `V` resultam de uma transformação PCA aplicada pela ULB
> sobre as features originais (não divulgadas por sigilo). São centradas e em
> escala comparável por construção — não precisam de re-scaling.

---

## Análise Estatística (NB01)

### Normalidade

| Teste | Resultado |
|---|---|
| D'Agostino-Pearson | **30/30 features** rejeitam normalidade (p < 0,05) |
| Implicação | Uso de testes **não-paramétricos** (Mann-Whitney) |

> O Shapiro-Wilk não se aplica (limite de ~5.000 amostras); com 284k linhas,
> o D'Agostino-Pearson é o teste adequado.

### Poder Discriminativo (Mann-Whitney U + tamanho de efeito)

| Feature | Efeito (\|rank-biserial\|) | Mediana fraude | Mediana legítima |
|---|---|---|---|
| `V14` | 0,898 | −6,73 | 0,05 |
| `V4` | 0,877 | 4,18 | −0,02 |
| `V12` | 0,874 | −5,50 | 0,14 |
| `V11` | 0,836 | 3,59 | −0,04 |
| `V10` | 0,828 | −4,58 | −0,09 |
| `V3` | 0,824 | −5,08 | 0,18 |

> Com 284k linhas, o p-valor é trivialmente significativo (até 1e-260) — por
> isso o **tamanho de efeito** é o que separa features úteis das fracas.
> 13 features têm efeito forte (> 0,5); 3 não têm significância.

### Amount e Time

| Feature | Mediana fraude | Mediana legítima | Leitura |
|---|---|---|---|
| `Amount` | £9,25 | £22,00 | Fraudes tendem a valores baixos (testes de cartão) |
| `Time` | absoluto | absoluto | Bimodal (dia/noite); não generaliza → descartado |

---

## Limpeza e Pré-processamento (NB02)

### Limpeza

| Ação | Critério | Registros afetados |
|---|---|---|
| Remoção de duplicatas | Linhas idênticas em todas as 31 colunas | 1.081 (incl. 19 fraudes) |
| **Nulos** | Nenhum | 0 registros |
| **Total após limpeza** | | **283.726 linhas · 473 fraudes** |

### Split Estratificado

| Conjunto | Linhas | Fraudes | % fraude |
|---|---|---|---|
| Treino | 226.980 | 378 | 0,167% |
| Teste | 56.746 | 95 | 0,167% |

> `stratify=Class` é obrigatório com classe rara — garante a mesma proporção
> de fraude nos dois conjuntos. O balanceamento **não** é aplicado no split, e
> sim dentro do CV (evita data leakage).

### Preprocessor (`pipeline_final.joblib`)

| Feature | Transformação | Motivo |
|---|---|---|
| `Amount` | RobustScaler | Robusto aos outliers (mediana/IQR, não média/desvio) |
| `V1` – `V28` | passthrough | Já são componentes PCA centrados |
| `Time` | descartado (`remainder='drop'`) | Valor absoluto, não generaliza |

> 29 features finais (28 V's + Amount). `set_output('pandas')` garante DataFrame
> nomeado — essencial para o SHAP e robustez no app.

---

## Estratégia de Balanceamento (NB03)

| Estratégia | PR-AUC | Recall | Precision |
|---|---|---|---|
| Sem balanceamento | 0,755 | 0,611 | 0,868 |
| class_weight='balanced' | 0,754 | 0,907 | 0,058 |
| SMOTE | 0,752 | 0,907 | 0,056 |
| SMOTE + Undersampling | 0,755 | 0,889 | 0,105 |

> **PR-AUC praticamente idêntico** nas 4 estratégias → as classes são
> separáveis o suficiente. O balanceamento muda o trade-off recall/precision,
> não o PR-AUC. Escolhida: `class_weight='balanced'` (não infla os dados).

---

## Modelo Final (NB04)

| Parâmetro | Valor | Descrição |
|---|---|---|
| Algoritmo | XGBoost | Vencedor do Optuna (40 trials, XGB vs RF) |
| n_estimators | 526 | nº de árvores |
| max_depth | 10 | profundidade (captura interações entre V's) |
| learning_rate | 0,094 | taxa de aprendizado |
| subsample | 0,727 | fração de amostras por árvore |
| colsample_bytree | 0,856 | fração de features por árvore |
| scale_pos_weight | 599 | peso da classe positiva (razão neg/pos) |
| Threshold | 0,264 | otimizado para máximo F1 |
| PR-AUC (teste) | 0,826 | métrica primária (desbalanceamento) |
| ROC-AUC (teste) | 0,974 | enganoso sob desbalanceamento extremo |
| Recall | 0,811 | 77 de 95 fraudes detectadas |
| Precision | 0,951 | apenas 4 falsos alarmes |

> **Threshold 0,264 (máximo F1):** abaixo do padrão 0,5 para capturar mais
> fraudes. Acima de ~80% de recall, a precision colapsa — limite estrutural do
> problema (as fraudes restantes são camufladas, indistinguíveis das legítimas).

---

## Interpretabilidade (NB05)

### Validação cruzada das features

| Método | Top 3 features |
|---|---|
| Mann-Whitney (EDA, univariado) | V14 > V4 > V12 |
| SHAP (importância global) | V14 > V4 > V12 |

> Três métodos independentes (tamanho de efeito, SHAP global, casos
> individuais) convergem nas mesmas variáveis — robustez real, não artefato.

### Casos individuais (o par que explica o recall)

| Caso | V14 | V4 | V12 | P(fraude) | Resultado |
|---|---|---|---|---|---|
| TP (detectada) | −13,69 | 8,93 | −13,06 | 1,000 | Assinatura extrema |
| FN (escapou) | −0,01 | 0,90 | 0,69 | 0,000 | Camuflada (≈ normal) |

> A fraude que escapa tem componentes PCA próximos dos valores legítimos
> (V14 ≈ 0, contra ≈ −13 nas fraudes óbvias). Os ~20% perdidos são fraudes
> desenhadas para imitar transações comuns — um teto estrutural, não falha
> de ajuste do modelo.
