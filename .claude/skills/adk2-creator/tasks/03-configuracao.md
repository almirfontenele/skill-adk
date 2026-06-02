# Task 03 — Configuração de Credenciais e Ambiente

## Objetivo
Solicitar a chave da API do Google de forma segura, gerar o arquivo `.env` e validar que o projeto está pronto para execução.

---

## Passo 1: Solicitar a chave da API

Pergunte ao usuário:

> "Para executar o agente, você precisa de uma chave da API do Google (GOOGLE_API_KEY).
> Você pode obtê-la em https://aistudio.google.com/apikey
> Cole a chave abaixo (ela não será exibida no output):"

**Nunca logue ou exiba a chave.** Use-a apenas para escrever no arquivo `.env`.

---

## Passo 2: Gerar o arquivo `.env`

Com a chave fornecida pelo usuário, crie o `.env`:

```bash
# Execute via Python para evitar que a chave apareça no histórico do shell
python - << 'EOF'
import os, getpass
key = getpass.getpass("GOOGLE_API_KEY: ")
with open(".env", "w") as f:
    f.write(f"GOOGLE_API_KEY={key}\n")
    f.write("MODEL_ID=gemini-2.5-flash\n")
    f.write(f"APP_NAME={os.path.basename(os.getcwd())}\n")
print(".env gerado com sucesso.")
EOF
```

Alternativamente, se o usuário já forneceu a chave na conversa:

```python
# Escreva diretamente via Write tool, sem expor a chave em bash history
```

---

## Passo 3: Validar o ambiente

Execute uma checagem rápida antes de rodar o projeto completo:

```bash
python - << 'EOF'
from dotenv import load_dotenv
import os, sys
load_dotenv()
key = os.getenv("GOOGLE_API_KEY", "")
if not key:
    print("ERRO: GOOGLE_API_KEY não encontrada no .env")
    sys.exit(1)
if len(key) < 20:
    print("AVISO: A chave parece inválida (muito curta)")
    sys.exit(1)
print(f"✓ GOOGLE_API_KEY configurada ({len(key)} chars)")
print(f"✓ MODEL_ID: {os.getenv('MODEL_ID', 'gemini-2.5-flash')}")
EOF
```

---

## Passo 4: Executar o projeto

```bash
python main.py
```

Se houver erro de autenticação (`401 Unauthorized` ou `API_KEY_INVALID`):
1. Verifique se o `.env` está na raiz do projeto
2. Confirme que a chave é válida em https://aistudio.google.com/apikey
3. Certifique-se de que `load_dotenv()` é chamado antes de qualquer import do ADK

---

## Boas Práticas de Segurança

- `.env` nunca deve ser commitado — confirme que está no `.gitignore`
- Use `.env.example` como template público (sem valores reais)
- Em produção, prefira variáveis de ambiente do sistema ou Secret Manager

---

## Verificação Final

- [ ] `.env` gerado com `GOOGLE_API_KEY` válida
- [ ] Checagem de ambiente passou sem erros
- [ ] `python main.py` executou e o agente respondeu
- [ ] `.env` está no `.gitignore`
