# 🚀 Checklist de Deploy — Streamlit Cloud

Sequência validada nos projetos do portfólio. Seguir na ordem evita os
erros que já custaram tempo (o `environment.yml`, a pasta `.streamlit`, etc.).

---

## 0. Setup inicial do projeto (ao clonar o templates_ds)

Os projetos compartilham o nome de pacote `src`. Quando você roda
`pip install -e .` num projeto novo, ele **sequestra** o import `src`
para o último projeto instalado — e os imports `from src.config import ...`
passam a apontar para o projeto errado (erro: `ImportError: cannot import
name ... from 'src.viz_config' (...OUTRO_PROJETO...)`).

- [ ] **`setup.py` na raiz** (o do template é genérico — deriva o nome da pasta)
- [ ] **Reinstalar apontando para ESTE projeto**, de dentro da pasta:
      ```powershell
      pip install -e . --force-reinstall --no-deps
      ```
      - `--force-reinstall` → reescreve o registro do `src` para este projeto
      - `--no-deps` → não reinstala pandas/sklearn/etc. (já estão no ambiente)
- [ ] **Reiniciar o kernel** do Jupyter (Kernel → Restart) — o Python
      mantém o `src` antigo em cache até reiniciar
- [ ] **Confirmar o caminho** numa célula:
      ```python
      import src.viz_config; print(src.viz_config.__file__)
      # deve apontar para ...\<ESTE_PROJETO>\src\viz_config.py
      ```

> Faça isso toda vez que **trocar de projeto** na mesma sessão de trabalho —
> o `src` instalado é global no ambiente conda, não por projeto.

---

## 1. Antes do commit

- [ ] **`scikit-learn` fixado** no `requirements.txt` na versão de treino
      → `python -c "import sklearn; print(sklearn.__version__)"`
- [ ] **`environment.yml` NÃO rastreado** (o Cloud o prioriza sobre o requirements.txt)
      → `git rm --cached environment.yml 2>$null`
      → confirmar que está no `.gitignore`
- [ ] **Pasta `.streamlit`** com ponto na frente (não `streamlit`)
      → contém `config.toml` com o tema
- [ ] **Artefatos versionados** (o app precisa deles):
      `models/*.joblib`, `models/*.pkl`, `models/*.json`,
      `data/processed/features.parquet`
- [ ] **Dados brutos NÃO versionados** (`data/raw/*.xlsx|csv` grandes)
- [ ] **Nenhum arquivo > 100 MB** (limite do GitHub)
      → `Get-ChildItem models, data\processed -Recurse -File | Select Name, @{N="MB";E={[math]::Round($_.Length/1MB,2)}} | Sort MB -Descending`
- [ ] **App não importa de `src/`** sem o pacote instalado
      (o Cloud não roda `pip install -e .`; o app deve importar de `app/`)
- [ ] **Paths deploy-safe**: `Path(__file__).resolve().parent.parent`,
      nunca caminhos absolutos nem `os.getcwd()`

## 2. Commit e push

```powershell
git add -A
git status                    # ← CONFERIR: sem environment.yml, sem .xlsx bruto
git commit -m "feat: <descrição>"
git push -u origin main
```

## 3. Streamlit Cloud

- [ ] [share.streamlit.io](https://share.streamlit.io) → **Create app** → from GitHub
- [ ] **Repository:** `jhastoledo/<projeto>`
- [ ] **Branch:** `main`
- [ ] **Main file path:** `app/main.py`  ← o ponto de entrada
- [ ] **Deploy** e acompanhar os logs

## 4. Erros comuns (e a causa real)

| Erro nos logs | Causa | Correção |
|---|---|---|
| `ModuleNotFoundError: plotly` (ou outra lib) | `environment.yml` sequestrou o build | `git rm --cached environment.yml` |
| `ModuleNotFoundError: utils` / `style` | path dos imports | `sys.path.append(str(Path(__file__).resolve().parent.parent))` |
| `ModuleNotFoundError: src` | app importa de `src/` (não instalado no Cloud) | mover a lógica para `app/utils.py` |
| Erro ao despicklar o modelo | versão do sklearn diferente do treino | fixar a versão no `requirements.txt` |
| Tema dark não aplica | pasta `streamlit/` sem o ponto | renomear para `.streamlit/` |
| `FileNotFoundError` no artefato | path absoluto ou artefato não versionado | path relativo + conferir `.gitignore` |

## 5. Pós-deploy

- [ ] Testar o app no ar (todas as páginas, upload se houver)
- [ ] Copiar a URL pública
- [ ] Atualizar o `README.md` com o link + badge de demo
      → `git commit -m "docs: adiciona link do app publicado"`
