"""
setup.py generico para projetos de portfolio DS.

Torna o pacote `src/` instalavel via:  pip install -e .

O nome do projeto e derivado automaticamente do nome da pasta raiz,
entao este arquivo NAO precisa ser editado a cada novo projeto.
Basta copiar para a raiz e rodar:

    pip install -e . --force-reinstall --no-deps

O --force-reinstall garante que o `src` aponte para ESTE projeto
(evita o conflito de varios projetos compartilharem o nome `src`).
Lembre de reiniciar o kernel do Jupyter apos instalar.
"""
from pathlib import Path
from setuptools import setup, find_packages

# Nome do projeto = nome da pasta raiz (ex.: 'credit_card_fraud')
NOME_PROJETO = Path(__file__).resolve().parent.name

# Le requirements.txt se existir (opcional)
req_path = Path(__file__).resolve().parent / "requirements.txt"
requisitos = []
if req_path.exists():
    for linha in req_path.read_text(encoding="utf-8").splitlines():
        linha = linha.split("#")[0].strip()   # remove comentarios inline
        if linha:
            requisitos.append(linha)

setup(
    name=NOME_PROJETO,
    version="0.1.0",
    description=f"Projeto de portfolio DS - {NOME_PROJETO}",
    author="Jhonnes Toledo",
    packages=find_packages(),          # acha o pacote `src` automaticamente
    install_requires=requisitos,
    python_requires=">=3.11",
)
