---
name: adk2-creator
description: >
  Scaffold and develop Python AI agent projects using Google ADK 2.0 (Agent Development Kit).
  Use this skill whenever the user wants to create, extend, or fix a Python project that uses
  the Google ADK library (google-adk), Gemini agents, function calling, async runners, tools,
  or session state. Also trigger when the user says "criar agente ADK", "novo projeto ADK",
  "quero usar gemini com tools", "agente com function calling", or mentions google-adk, ADK 2.0,
  InMemorySessionService, or Runner in a Python context.
---

# ADK 2.0 Creator

Skill para scaffolding e desenvolvimento de projetos Python com Google ADK 2.0.
Segue boas práticas: tipagem, estrutura limpa, async nativo e function calling automático.

## Fluxo de Execução

Siga as tasks na ordem abaixo. Cada arquivo tem instruções detalhadas — leia antes de executar a etapa.

1. **Setup** → `tasks/01-setup.md`
2. **Implementação** → `tasks/02-implementacao.md`
3. **Configuração** → `tasks/03-configuracao.md`

## Estrutura de Projeto Gerada

```
<nome-do-projeto>/
├── src/
│   ├── agents/         # Classe do agente (herda de Agent ou usa composição)
│   ├── tools/          # Funções de tool (plain Python async)
│   ├── schemas/        # Pydantic models de input/output
│   └── config.py       # Leitura de env vars via python-dotenv
├── main.py             # Ponto de entrada com runner async
├── pyproject.toml      # Dependências (uv ou pip)
├── .env.example        # Template de variáveis de ambiente
└── README.md
```

## Princípios Obrigatórios

- **Async nativo**: toda interação com o runner usa `async/await`
- **Function calling automático**: ferramentas são plain Python `async def` com docstring e type hints — o ADK registra automaticamente
- **Sessão explícita**: sempre criar sessão via `InMemorySessionService` antes de invocar o runner
- **Tipagem completa**: parâmetros e retornos tipados em todas as funções

## Referências de Código

- Snippets reais de chat, histórico e function calling → `referencias/snippets-adk2.md`
- Análise dos 3 principais gargalos de prompts genéricos → `referencias/gargalos.md`
