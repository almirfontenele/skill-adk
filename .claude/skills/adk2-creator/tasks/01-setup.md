# Task 01 — Setup do Projeto ADK 2.0

## Objetivo
Inicializar o ambiente de desenvolvimento com estrutura de diretórios, controle de versão e dependências mínimas para um projeto ADK 2.0.

---

## Passo 1: Criar estrutura de diretórios

```bash
mkdir -p <nome-do-projeto>/{src/{agents,tools,schemas},tests}
cd <nome-do-projeto>
```

Crie os arquivos `__init__.py` em cada subpacote:
```bash
touch src/__init__.py src/agents/__init__.py src/tools/__init__.py src/schemas/__init__.py
```

---

## Passo 2: Inicializar repositório Git

```bash
git init
cat > .gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
.env
*.egg-info/
dist/
.pytest_cache/
EOF
git add .gitignore
git commit -m "chore: initial project setup"
```

---

## Passo 3: Criar `pyproject.toml`

Prefira `uv` quando disponível (`which uv`). Caso não, use `pip + venv`.

### Com uv
```bash
uv init --no-workspace
uv add google-adk pydantic python-dotenv
```

### Com pip
Crie `pyproject.toml` manualmente:
```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "<nome-do-projeto>"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "google-adk>=2.0.0a1",
    "pydantic>=2.7",
    "python-dotenv>=1.0",
]
```

Depois:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows
pip install -e .
```

---

## Passo 4: Criar `src/config.py`

```python
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY: str = os.environ["GOOGLE_API_KEY"]
MODEL_ID: str = os.getenv("MODEL_ID", "gemini-2.5-flash")
APP_NAME: str = os.getenv("APP_NAME", "<nome-do-projeto>")
```

---

## Passo 5: Criar `.env.example`

```
GOOGLE_API_KEY=
MODEL_ID=gemini-2.5-flash
APP_NAME=<nome-do-projeto>
```

---

## Verificação

- [ ] Diretórios `src/agents/`, `src/tools/`, `src/schemas/` criados
- [ ] `pyproject.toml` com `google-adk`, `pydantic`, `python-dotenv`
- [ ] `.venv` ativo e pacotes instaláveis
- [ ] `src/config.py` lendo variáveis de ambiente
- [ ] `.env.example` com `GOOGLE_API_KEY` vazio
- [ ] `.gitignore` excluindo `.env` e `.venv`

Próxima etapa → `tasks/02-implementacao.md`
