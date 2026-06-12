"""
Gerador de relatórios HTML reutilizável (tema GitHub Dark).

Componentes genéricos para qualquer projeto do portfólio. O CONTEÚDO
(textos, métricas, figuras) vem do notebook; o módulo cuida da
estrutura, do tema e do embutimento de imagens em base64.

Uso:
    from src.report import RelatorioHTML

    rel = (RelatorioHTML("Título", autor="Jhonnes Toledo", subtitulo="...")
           .add_secao("Visão geral", "<p>texto...</p>")
           .add_metricas({"Silhouette ↑": 0.428, "DB ↓": 0.825})
           .add_tabela(df_resumo, titulo="Personas")
           .add_figuras([(caminho_png, "legenda")])
           .salvar(caminho_html))
"""
import base64
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.viz_config import CORES   # fonte única do tema


class RelatorioHTML:
    """Constrói um relatório HTML de página única com tema GitHub Dark."""

    def __init__(self, titulo: str, autor: str = "", subtitulo: str = ""):
        self.titulo = titulo
        self.autor = autor
        self.subtitulo = subtitulo
        self._blocos: list[str] = []   # corpo acumulado

    # ── Componentes (encadeáveis: cada um retorna self) ──────────

    def add_secao(self, titulo: str, html_conteudo: str) -> "RelatorioHTML":
        """Seção com título <h2> e conteúdo HTML livre."""
        self._blocos.append(f"<h2>{titulo}</h2>{html_conteudo}")
        return self

    def add_card(self, html_conteudo: str) -> "RelatorioHTML":
        """Bloco destacado (caixa com borda)."""
        self._blocos.append(f"<div class='card'>{html_conteudo}</div>")
        return self

    def add_metricas(self, metricas: dict) -> "RelatorioHTML":
        """Linha de cards de métrica a partir de {rótulo: valor}."""
        cards = "".join(
            f"<div class='metrica'><span class='valor'>{v}</span><br>"
            f"<span class='rotulo'>{rotulo}</span></div>"
            for rotulo, v in metricas.items()
        )
        self._blocos.append(f"<div>{cards}</div>")
        return self

    def add_tabela(self, df: pd.DataFrame, titulo: str = "",
                   incluir_indice: bool = True) -> "RelatorioHTML":
        """Tabela zebrada a partir de um DataFrame."""
        cols = ([df.index.name or ""] if incluir_indice else []) + list(df.columns)
        cabecalho = "".join(f"<th>{c}</th>" for c in cols)
        linhas = ""
        for idx, row in df.iterrows():
            celulas = ([f"<td>{idx}</td>"] if incluir_indice else []) + \
                      [f"<td>{v}</td>" for v in row]
            linhas += f"<tr>{''.join(celulas)}</tr>"
        bloco = ""
        if titulo:
            bloco += f"<h3>{titulo}</h3>"
        bloco += f"<table><tr>{cabecalho}</tr>{linhas}</table>"
        self._blocos.append(bloco)
        return self

    def add_figuras(self, figuras: list) -> "RelatorioHTML":
        """
        Embute figuras em base64 (arquivo autossuficiente).
        figuras: lista de (caminho_png, legenda).
        """
        for caminho, legenda in figuras:
            caminho = Path(caminho)
            if not caminho.exists():
                self._blocos.append(
                    f"<p style='color:{CORES['vermelho']}'>"
                    f"⚠️ figura não encontrada: {caminho.name}</p>")
                continue
            b64 = base64.b64encode(caminho.read_bytes()).decode("utf-8")
            self._blocos.append(
                f"<figure><img src='data:image/png;base64,{b64}' "
                f"alt='{legenda}'><figcaption>{legenda}</figcaption></figure>")
        return self

    def add_html(self, html_livre: str) -> "RelatorioHTML":
        """Insere HTML arbitrário (escape hatch)."""
        self._blocos.append(html_livre)
        return self

    # ── Renderização ─────────────────────────────────────────────

    def _css(self) -> str:
        c = CORES
        return f"""<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:{c['fundo']}; color:{c['texto']};
    font-family:'Segoe UI',-apple-system,sans-serif; line-height:1.6;
    max-width:1000px; margin:0 auto; padding:40px 24px; }}
  h1 {{ color:{c['azul']}; font-size:2.2em;
    border-bottom:2px solid {c['borda']}; padding-bottom:16px; margin-bottom:8px; }}
  h2 {{ color:{c['azul']}; font-size:1.5em; margin:36px 0 12px;
    padding-left:12px; border-left:4px solid {c['azul']}; }}
  h3 {{ color:{c['roxo']}; font-size:1.15em; margin:20px 0 8px; }}
  p, li {{ color:{c['texto']}; margin-bottom:8px; }}
  .subtitulo {{ color:{c['texto2']}; font-size:1.05em; margin-bottom:4px; }}
  .meta {{ color:{c['texto2']}; font-size:0.9em; }}
  code {{ background:{c['surf']}; color:{c['laranja']}; padding:2px 6px;
    border-radius:4px; font-family:'JetBrains Mono',monospace; font-size:0.9em; }}
  .card {{ background:{c['surf']}; border:1px solid {c['borda']};
    border-radius:8px; padding:16px 20px; margin:12px 0; }}
  .metrica {{ display:inline-block; background:{c['surf']};
    border:1px solid {c['borda']}; border-radius:6px;
    padding:10px 18px; margin:6px 8px 6px 0; }}
  .metrica .valor {{ color:{c['verde']}; font-size:1.4em; font-weight:bold; }}
  .metrica .rotulo {{ color:{c['texto2']}; font-size:0.85em; }}
  figure {{ margin:20px 0; text-align:center; }}
  figure img {{ max-width:100%; border:1px solid {c['borda']}; border-radius:8px; }}
  figcaption {{ color:{c['texto2']}; font-size:0.9em; margin-top:8px; }}
  table {{ border-collapse:collapse; width:100%; margin:16px 0; }}
  th, td {{ border:1px solid {c['borda']}; padding:8px 12px; text-align:left; }}
  th {{ background:{c['surf']}; color:{c['azul']}; }}
  tr:nth-child(even) {{ background:{c['surf']}; }}
  .badge {{ display:inline-block; background:{c['azul']}; color:{c['fundo']};
    padding:2px 10px; border-radius:12px; font-size:0.8em; font-weight:bold; }}
  footer {{ margin-top:48px; padding-top:16px; border-top:1px solid {c['borda']};
    color:{c['texto2']}; font-size:0.85em; text-align:center; }}
</style>"""

    def _cabecalho(self) -> str:
        h = f"<h1>{self.titulo}</h1>"
        if self.subtitulo:
            h += f"<p class='subtitulo'>{self.subtitulo}</p>"
        meta = []
        if self.autor:
            meta.append(self.autor)
        meta.append(f"gerado em {datetime.now():%d/%m/%Y}")
        h += f"<p class='meta'>{' · '.join(meta)}</p>"
        return h

    def render(self) -> str:
        corpo = self._cabecalho() + "".join(self._blocos)
        return (f"<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'>"
                f"{self._css()}</head><body>{corpo}</body></html>")

    def salvar(self, caminho) -> Path:
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(self.render(), encoding="utf-8")
        return caminho