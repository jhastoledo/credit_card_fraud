"""
Carrega as configurações centralizadas do projeto a partir de configs/config.yaml.
Uso:
    from src.config import CONFIG, CAMINHOS
    df = pd.read_csv(CAMINHOS.dados_raw / "seu_arquivo.csv")
    target = CONFIG["dados"]["target_col"]
"""
from pathlib import Path
import yaml

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent


def _carregar_yaml(caminho: Path) -> dict:
    if not caminho.exists():
        raise FileNotFoundError(f"[config.py] Arquivo não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


_config = _carregar_yaml(ROOT / "configs" / "config.yaml")


class _Caminhos:
    """Acesso dinâmico aos caminhos do config.yaml.
    Pastas → Path absoluto; arquivos (contêm '.') → string."""
    def __getattr__(self, chave: str):
        caminhos = _config.get("caminhos", {})
        if chave not in caminhos:
            raise AttributeError(
                f"Caminho '{chave}' não encontrado em config.yaml.\n"
                f"Chaves disponíveis: {list(caminhos.keys())}"
            )
        valor = caminhos[chave]
        if "." in str(valor):
            return valor
        return ROOT / valor


CONFIG   = _config
CAMINHOS = _Caminhos()
