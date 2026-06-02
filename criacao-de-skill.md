# Criação de Skill - ADK 2.0 (Agent Development Kit)

## Objetivo

Criar uma skill com habilidade de desenvolver aplicações de agentes usando:

- **Python**: boas práticas, tipagem e estrutura limpa
- **ADK 2.0**: manipulação correta das APIs do Gemini

## Referências

- https://github.com/google/adk-python/tree/v2/contributing/workflow_samples
- https://github.com/google/adk-python/blob/v2/pyproject.toml

## Tasks a Gerar: as tasks devem ser criadas em subpasta tasks e referencias para Uso na SKILL.md

 
### Setup

[ ] Criar projeto ADK 2.0 em Python: Iniciar repositório Git e configurar o ambiente virtual.

[ ] Instalar dependências mínimas: Incluir google-adk, pydantic e python-dotenv no gerenciador de pacotes (pip ou uv).

[ ] Montar estrutura de diretórios: Criar as pastas src/agents, src/tools, src/schemas, o arquivo de configuração src/config.py e o main.py.
[ ] Iniciar git repository se necessário

### Implementação

[ ] Desenvolver agente básico: Implementar o agente com o modelo gemini-2.5-flash integrado a uma ferramenta nativa simples.
[ ] Criar documentação e ambiente: Escrever o README.md com instruções de execução e o arquivo .env.example com a variável GOOGLE_API_KEY=.
[ ] Configuração de credenciais: Solicitar a chave da API do Google em tempo de execução e gerar o arquivo .env local.

### Configuração

- [ ] Pedir a chave Google
- [ ] Gerar arquivo `.env`


## Inserção de Snippets de Referência

Adicionar ao `SKILL.md` referencias em arquivos exemplos reais e enxutos de código do ADK 2.0 na subpasta referencias, incluindo:

[ ]Chamadas de chat com histórico
[ ] Inserção de Snippets de Referência: Adicionar exemplos reais e enxutos de chamadas de chat com histórico, uso do modelo correto e Function Calling usando a API assíncrona do ADK 2.0.

[ ] Análise de Gargalos: Mapear e listar no arquivo os 3 principais gargalos de prompts genéricos, justificando o ganho de tempo e a assertividade obtidos com o novo SDK.

## Análise de Gargalos

Mapear e listar os 3 principais gargalos de prompts genéricos, justificando o ganho de tempo e assertividade com o uso do novo SDK documentado no arquivo
