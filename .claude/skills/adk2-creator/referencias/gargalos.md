# Análise de Gargalos — Prompts Genéricos vs ADK 2.0

Os 3 principais gargalos ao usar prompts genéricos (sem SDK/framework) para construir agentes com Gemini, e como o ADK 2.0 elimina cada um.

---

## Gargalo 1: Gerenciamento Manual de Histórico de Conversa

### O problema
Sem framework, o desenvolvedor precisa montar manualmente a lista de mensagens a cada turno:

```python
# ❌ Abordagem genérica — frágil e trabalhosa
history = []

def chat(user_input: str) -> str:
    history.append({"role": "user", "parts": [{"text": user_input}]})
    response = model.generate_content(history)
    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text
```

Problemas reais desta abordagem:
- Sem limites de tamanho → o contexto cresce até estourar o limite de tokens
- Sem persistência → história perdida ao reiniciar o processo
- Sem isolamento → múltiplos usuários compartilham o mesmo `history`

### Como o ADK 2.0 resolve
`InMemorySessionService` gerencia histórico por `(app_name, user_id, session_id)` automaticamente. O runner injeta o histórico correto a cada chamada, sem nenhum código extra do desenvolvedor.

```python
# ✅ ADK 2.0 — histórico automático e isolado por sessão
session = await session_service.create_session(app_name=APP_NAME, user_id="alice")
# A partir daqui, o runner mantém o histórico automaticamente
```

**Ganho**: elimina ~30-50 linhas de boilerplate por projeto e previne bugs de contaminação entre usuários.

---

## Gargalo 2: Implementação Manual de Function Calling

### O problema
A API Gemini suporta function calling, mas exige definição manual do schema JSON para cada ferramenta:

```python
# ❌ Abordagem genérica — muito boilerplate por ferramenta
tools = [{
    "function_declarations": [{
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }]
}]

# E ainda precisa parsear manualmente a resposta e despachar a chamada:
response = model.generate_content(prompt, tools=tools)
if response.candidates[0].content.parts[0].function_call:
    call = response.candidates[0].content.parts[0].function_call
    if call.name == "get_weather":
        result = get_weather(**call.args)
    # ... enviar result de volta, lidar com loop de tool use ...
```

### Como o ADK 2.0 resolve
Qualquer `async def` com type hints e docstring vira uma ferramenta automaticamente. O ADK gera o schema, despacha as chamadas, coleta os resultados e continua o loop — tudo transparente:

```python
# ✅ ADK 2.0 — zero boilerplate de tool use
async def get_weather(city: str) -> dict:
    """Get current weather for a city."""
    return {"temp": 22, "city": city}

agent = Agent(model="gemini-2.5-flash", tools=[get_weather])
```

**Ganho**: reduz o código de integração de ferramentas de ~40-80 linhas para ~1 linha por ferramenta. Elimina erros de schema incompatível e bugs no loop de tool use.

---

## Gargalo 3: Orquestração do Loop de Execução

### O problema
Agentes reais precisam de múltiplos ciclos modelo→ferramenta→modelo antes de gerar a resposta final. Implementar esse loop manualmente é propenso a erros:

```python
# ❌ Abordagem genérica — loop manual frágil
max_iterations = 10
for _ in range(max_iterations):
    response = model.generate_content(messages, tools=tools)
    part = response.candidates[0].content.parts[0]
    
    if hasattr(part, "function_call"):
        # despachar tool, adicionar resultado ao histórico, continuar
        ...
    elif part.text:
        return part.text  # resposta final
    else:
        break  # estado inesperado — e agora?
```

Problemas: sem tratamento de erros de tool, sem timeout, sem limite de ciclos configurável, sem eventos para observabilidade.

### Como o ADK 2.0 resolve
O `Runner` executa o loop completo internamente e emite eventos tipados a cada etapa. O desenvolvedor apenas consome o stream:

```python
# ✅ ADK 2.0 — loop gerenciado, eventos tipados
async for event in runner.run_async(user_id=uid, session_id=sid, new_message=msg):
    if event.is_final_response():
        print(event.content.parts[0].text)
    elif event.get_function_calls():
        # opcional: logging de observabilidade
        for call in event.get_function_calls():
            print(f"[tool] {call.name}")
```

**Ganho**: elimina bugs de loop infinito, trata edge cases de tool use automaticamente, e fornece observabilidade granular sem custo adicional. Em projetos com 3+ ferramentas, isso representa ~100 linhas de lógica de orquestração eliminadas.

---

## Resumo

| Gargalo | Linhas sem ADK | Linhas com ADK 2.0 | Ganho |
|---------|---------------|---------------------|-------|
| Histórico de sessão | ~40 | ~3 | 92% menos código |
| Schema de ferramentas | ~15 por tool | 0 por tool | 100% eliminado |
| Loop de orquestração | ~60 | ~5 | 91% menos código |

O principal ganho não é só em linhas de código, mas em **assertividade**: sem ADK, cada projeto reinventa esses mecanismos com bugs sutis diferentes. Com ADK 2.0, esses comportamentos são testados pela biblioteca e se comportam de forma previsível.
