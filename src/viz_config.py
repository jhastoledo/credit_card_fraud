# src/viz_config.py
# ================================================================
# Configuracoes globais de visualizacao - GitHub Dark Theme
# Importar nos notebooks com:
#   from src.viz_config import aplicar_tema, PALETTE, CORES
#   from src.viz_config import aplicar_tema_seaborn   # se usar seaborn
# ================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl

# --- Paleta principal -------------------------------------------
PALETTE = ['#58a6ff', '#ff7b72', '#3fb950', '#d2a8ff', '#ffa657',
           '#79c0ff', '#ffa198', '#56d364', '#e3b341', '#f78166']

# --- Cores semanticas -------------------------------------------
CORES = {
    'azul':     '#58a6ff',   # titulos, destaques principais
    'verde':    '#3fb950',   # positivo, sucesso, concluido
    'roxo':     '#d2a8ff',   # funcoes, metodos, derivadas
    'laranja':  '#ffa657',   # alertas, atencao
    'vermelho': '#ff7b72',   # erros, armadilhas, negativo
    'amarelo':  '#e3b341',   # neutro, informativo
    'texto':    '#e6edf3',   # texto principal
    'texto2':   '#8b949e',   # texto secundario
    'fundo':    '#0d1117',   # background
    'surf':     '#161b22',   # surface
    'borda':    '#30363d',   # bordas
}

# --- Tema matplotlib --------------------------------------------
def aplicar_tema():
    """Aplica o tema GitHub Dark em todos os plots matplotlib."""
    plt.rcParams.update({
        # Fundos
        'figure.facecolor':  CORES['fundo'],
        'axes.facecolor':    CORES['surf'],
        'savefig.facecolor': CORES['fundo'],

        # Bordas e labels
        'axes.edgecolor':    CORES['borda'],
        'axes.labelcolor':   CORES['texto'],
        'axes.titlecolor':   CORES['texto'],

        # Ticks
        'xtick.color':       CORES['texto2'],
        'ytick.color':       CORES['texto2'],

        # Grid
        'grid.color':        '#21262d',
        'grid.linewidth':    0.6,
        'axes.grid':         True,

        # Texto
        'text.color':        CORES['texto'],
        'font.family':       'monospace',
        'font.size':         11,
        'axes.titlesize':    12,
        'axes.labelsize':    10,

        # Legenda
        'legend.facecolor':  CORES['surf'],
        'legend.edgecolor':  CORES['borda'],
        'legend.labelcolor': CORES['texto'],
        'legend.fontsize':   9,

        # Figura
        'figure.dpi':        100,
        'figure.titlesize':  13,

        # Linhas
        'lines.linewidth':   1.8,

        # Colormap padrao
        'image.cmap':        'viridis',
    })
    # Paleta padrao do ciclo de cores
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=PALETTE)


# --- Integracao com Seaborn -------------------------------------
def aplicar_tema_seaborn(style: str = "darkgrid"):
    """
    Aplica o tema GitHub Dark ao Seaborn, herdando as cores do viz_config.
    Chama aplicar_tema() antes para alinhar o matplotlib base.

    Uso:
        from src.viz_config import aplicar_tema_seaborn, PALETTE, CORES
        aplicar_tema_seaborn()

    O import de seaborn fica dentro da funcao de proposito: assim o
    viz_config continua importavel em projetos que nao usam seaborn.
    """
    import seaborn as sns

    aplicar_tema()
    sns.set_theme(style=style, rc={
        "figure.facecolor":  CORES["fundo"],
        "axes.facecolor":    CORES["surf"],
        "axes.edgecolor":    CORES["borda"],
        "axes.labelcolor":   CORES["texto"],
        "axes.titlecolor":   CORES["texto"],
        "text.color":        CORES["texto"],
        "xtick.color":       CORES["texto2"],
        "ytick.color":       CORES["texto2"],
        "grid.color":        "#21262d",
        "font.family":       "monospace",
    })
    sns.set_palette(PALETTE)


# --- Aplicar automaticamente ao importar ------------------------
aplicar_tema()
