# Snippets de Referência — ADK 2.0

Exemplos reais e enxutos para uso direto em projetos ADK 2.0.

---

## 1. Chat com Histórico (Multi-turn)

O histórico é mantido automaticamente por sessão. Use o mesmo `session_id` e `user_id` para garantir continuidade.

```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents import Agent
from google.genai import types

async def multi_turn_chat():
    agent = Agent(
        name="chat_agent",
        model="gemini-2.5-flash",
        instruction="Você é um assistente conversacional.",
    )
    session_service = InMemorySessionService()
    runner = Runner(agent=agent, app_name="chat", session_service=session_service)

    session = await session_service.create_session(app_name="chat", user_id="alice")

    prompts = [
        "Meu nome é Alice.",
        "Qual é o meu nome?",  # Deve lembrar "Alice"
    ]

    for prompt in prompts:
        msg = types.Content(role="user", parts=[types.Part(text=prompt)])
        async for event in runner.run_async(
            user_id="alice",
            session_id=session.id,
            new_message=msg,
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agente: {part.text}")

asyncio.run(multi_turn_chat())
```

**Ponto-chave**: `session.id` e `user_id="alice"` são fixos entre turnos — o `InMemorySessionService` acumula os eventos e o modelo recebe o histórico completo.

---

## 2. Function Calling Automático

O ADK 2.0 registra ferramentas a partir de funções Python async com type hints e docstring. Nenhuma configuração extra é necessária.

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio


async def get_weather(city: str) -> dict:
    """Get current weather conditions for a city.

    Args:
        city: City name (e.g. 'São Paulo').

    Returns:
        Dictionary with temperature_celsius and condition.
    """
    # Simulação — substitua por chamada real à API
    return {"temperature_celsius": 22, "condition": "partly cloudy", "city": city}


async def main():
    agent = Agent(
        name="weather_agent",
        model="gemini-2.5-flash",
        instruction="Use a ferramenta get_weather para responder sobre o clima.",
        tools=[get_weather],  # <-- registro automático
    )
    session_service = InMemorySessionService()
    runner = Runner(agent=agent, app_name="weather", session_service=session_service)
    session = await session_service.create_session(app_name="weather", user_id="u1")

    msg = types.Content(role="user", parts=[types.Part(text="Como está o clima em Curitiba?")])
    async for event in runner.run_async(user_id="u1", session_id=session.id, new_message=msg):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

asyncio.run(main())
```

---

## 3. API Assíncrona — Capturando Eventos do Runner

O `runner.run_async` é um gerador assíncrono que emite vários tipos de evento. Para a maioria dos usos, filtre apenas `is_final_response()`.

```python
async for event in runner.run_async(
    user_id=user_id,
    session_id=session_id,
    new_message=message,
):
    # Resposta final do modelo (texto)
    if event.is_final_response():
        if event.content:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

    # Chamada de ferramenta (para logging/debug)
    elif event.get_function_calls():
        for call in event.get_function_calls():
            print(f"[tool] {call.name}({call.args})")

    # Resultado de ferramenta
    elif event.get_function_responses():
        for resp in event.get_function_responses():
            print(f"[tool result] {resp.name}: {resp.response}")
```

---

## 4. Estado de Sessão com ToolContext

Para persistir dados entre chamadas de ferramenta dentro de uma mesma sessão:

```python
from google.adk.tools import ToolContext

async def add_to_cart(item: str, tool_context: ToolContext) -> str:
    """Add an item to the shopping cart stored in session state.

    Args:
        item: Product name to add.
        tool_context: Injected automatically by ADK — do not pass manually.

    Returns:
        Confirmation with cart size.
    """
    cart: list[str] = tool_context.state.get("cart", [])
    cart.append(item)
    tool_context.state["cart"] = cart
    return f"'{item}' adicionado. Carrinho tem {len(cart)} item(s)."
```

`ToolContext` é injetado pelo ADK automaticamente — basta incluir no tipo do parâmetro.

---

## 5. Modelo com Interactions API (streaming stateful)

Para conversas stateful com suporte a streaming nativo:

```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

agent = Agent(
    name="stateful_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        use_interactions_api=True,
    ),
    instruction="Assistente com memória de conversa.",
    tools=[get_weather],
)
```

Use esta opção quando precisar de streaming real ou quando a conversa for muito longa (reduz tokens re-enviados).

---

## Imports de Referência Rápida

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
from google.adk.models.google_llm import Gemini
from google.genai import types
```
