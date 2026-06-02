# Task 02 — Implementação do Agente ADK 2.0

## Objetivo
Implementar o agente básico com `gemini-2.5-flash`, ferramentas via function calling automático, e o runner assíncrono com histórico de sessão.

---

## Passo 1: Criar schema de domínio em `src/schemas/`

Crie um arquivo por entidade de domínio. Exemplo para um agente de tarefas:

```python
# src/schemas/task.py
from pydantic import BaseModel

class TaskInput(BaseModel):
    description: str
    priority: int = 1

class TaskResult(BaseModel):
    id: str
    status: str
    message: str
```

---

## Passo 2: Implementar ferramentas em `src/tools/`

Regras importantes para ADK 2.0:
- Funções devem ser `async def`
- Parâmetros tipados — o ADK usa os type hints para gerar o schema do function calling
- Docstring é obrigatória — é usada como descrição da ferramenta para o modelo
- Retorne `str` ou `dict` para respostas simples; use `pydantic` para estruturas complexas

```python
# src/tools/example_tools.py
async def get_current_time(timezone: str = "UTC") -> str:
    """Return the current time in the specified timezone.

    Args:
        timezone: IANA timezone name (e.g. 'America/Sao_Paulo').

    Returns:
        Current time as ISO 8601 string.
    """
    from datetime import datetime, timezone as tz
    import zoneinfo
    try:
        zone = zoneinfo.ZoneInfo(timezone)
        now = datetime.now(zone)
    except Exception:
        now = datetime.now(tz.utc)
    return now.isoformat()


async def calculate(expression: str) -> str:
    """Evaluate a safe arithmetic expression and return the result.

    Args:
        expression: A numeric expression string, e.g. '2 + 2 * 10'.

    Returns:
        Result as string, or error message if invalid.
    """
    import ast
    allowed = {ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub}
    try:
        tree = ast.parse(expression, mode='eval')
        if not all(type(node) in allowed for node in ast.walk(tree)):
            return "Expressão não permitida"
        result = eval(compile(tree, '<string>', 'eval'))  # noqa: S307
        return str(result)
    except Exception as e:
        return f"Erro: {e}"
```

---

## Passo 3: Implementar o agente em `src/agents/`

```python
# src/agents/main_agent.py
from google.adk.agents import Agent
from src.config import MODEL_ID
from src.tools.example_tools import get_current_time, calculate


def create_agent() -> Agent:
    """Factory function for the main agent."""
    return Agent(
        name="main_agent",
        model=MODEL_ID,
        instruction=(
            "Você é um assistente prestativo. "
            "Use as ferramentas disponíveis para responder com precisão."
        ),
        tools=[get_current_time, calculate],
    )
```

---

## Passo 4: Criar `main.py`

```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from src.agents.main_agent import create_agent
from src.config import APP_NAME


async def run_conversation(prompts: list[str]) -> None:
    agent = create_agent()
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="user_01",
    )

    for prompt in prompts:
        print(f"\n> {prompt}")
        message = types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )
        async for event in runner.run_async(
            user_id="user_01",
            session_id=session.id,
            new_message=message,
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        print(part.text)


if __name__ == "__main__":
    asyncio.run(run_conversation([
        "Qual é a hora agora em America/Sao_Paulo?",
        "Quanto é 125 * 48 + 300?",
    ]))
```

---

## Passo 5: Criar `README.md`

```markdown
# <Nome do Projeto>

Agente Python construído com Google ADK 2.0 e Gemini 2.5 Flash.

## Requisitos

- Python 3.11+
- uv (recomendado) ou pip

## Instalação

```bash
uv sync          # ou: pip install -e .
cp .env.example .env
# Edite .env e insira sua GOOGLE_API_KEY
```

## Execução

```bash
python main.py
```
```

---

## Verificação

- [ ] `src/tools/` com funções async tipadas e com docstring
- [ ] `src/agents/main_agent.py` com factory function retornando `Agent`
- [ ] `main.py` com runner assíncrono, sessão explícita e loop de eventos
- [ ] `README.md` com instruções de instalação e execução

Próxima etapa → `tasks/03-configuracao.md`
