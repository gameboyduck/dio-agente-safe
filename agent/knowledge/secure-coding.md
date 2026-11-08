# Programação segura em Python

Padrões defensivos para o código que o agente revisa ou escreve. Os exemplos são curtos de propósito: o objetivo é mostrar a causa da falha e a correção que ataca essa causa.

## Princípios

1. **Trate toda entrada externa como não confiável.** Isso inclui corpo de requisição, query string, cabeçalhos, arquivos, variáveis de ambiente, mensagens de fila e resposta de serviços externos.
2. **Não concatene dados em linguagens estruturadas.** SQL, shell, HTML, JSON e caminhos de arquivo têm regras próprias de codificação.
3. **Valide o formato e o tamanho, mas não dependa só disso.** Validação não substitui parametrização, codificação de saída ou autorização.
4. **Aplique privilégio mínimo.** Contas de banco, tokens, processos e usuários devem ter apenas o necessário.
5. **Falhe de forma segura.** Erros não devem expor stack trace, segredo ou detalhe interno ao usuário.
6. **Registre o necessário, sem segredos.** Log é evidência, não depósito de dados sensíveis.
7. **Mantenha dependências atualizadas e verificadas.** Uma dependência vulnerável é parte do seu código.

## SQL Injection

**Inseguro:**

```python
query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

**Seguro:**

```python
cursor.execute(
    "SELECT id, password_hash, salt FROM users WHERE username = ?",
    (username,),
)
```

O marcador `?` faz o driver tratar o valor como dado. A correção é uma consulta parametrizada: a estrutura SQL é fixa e o valor viaja separado. Não use interpolação, `%`, `format` ou concatenação para montar a consulta. Para nomes de tabela ou coluna, que não podem ser parametrizados, use uma allowlist fixa.

Em aplicações reais, não armazene nem compare senhas em texto puro. O exemplo acima busca o hash e a salt para verificar com uma função de derivação de chave.

## Senhas e segredos

**Inseguro:**

```python
if user.password == password:
    ...
```

**Seguro (biblioteca padrão, para fins didáticos):**

```python
import hmac
import hashlib

def verify_password(password: str, salt: bytes, expected_hash: bytes) -> bool:
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600_000)
    return hmac.compare_digest(candidate, expected_hash)
```

Em produção, prefira **Argon2id** (`argon2-cffi`) ou `scrypt`, com parâmetros calibrados. Use salt única por usuário, compare com `hmac.compare_digest` e nunca registre a senha.

Segredos devem vir de um gerenciador de segredos ou de variáveis de ambiente, nunca do repositório. Adicione `.env` ao `.gitignore` e forneça um `.env.example` sem valores reais.

## Injeção de comando

**Inseguro:**

```python
import os
os.system(f"convert {filename} output.png")
```

**Seguro:**

```python
import subprocess

subprocess.run(
    ["convert", filename, "output.png"],
    check=True,
    shell=False,
    timeout=30,
)
```

Evite `shell=True`. Se a ferramenta exigir shell, valide a entrada com allowlist e nunca interpole dados não confiáveis.

## Path traversal

**Inseguro:**

```python
path = os.path.join(BASE_DIR, user_filename)
return open(path).read()
```

**Seguro:**

```python
from pathlib import Path

base = Path(BASE_DIR).resolve()
candidate = (base / user_filename).resolve()

if base not in candidate.parents:
    raise ValueError("caminho fora do diretório permitido")

return candidate.read_text()
```

Verifique o caminho resolvido, não apenas o texto recebido. Rejeite caminhos absolutos e sequências de subida de diretório quando não forem necessários.

## Desserialização

**Inseguro:**

```python
import pickle
data = pickle.loads(request.body)
```

**Seguro:**

```python
import json
data = json.loads(request.body)
```

Nunca use `pickle`, `marshal` ou `yaml.load` com dados não confiáveis. Prefira JSON e `yaml.safe_load`. Se precisar de serialização binária, use formato com esquema e validação.

## Autorização

**Inseguro:**

```python
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return db.get_order(order_id)
```

**Seguro:**

```python
@app.get("/orders/{order_id}")
def get_order(order_id: int, current_user: User = Depends(require_user)):
    order = db.get_order(order_id)
    if order is None or order.owner_id != current_user.id:
        raise HTTPException(status_code=404)
    return order
```

Autenticação não é autorização. Verifique a permissão no recurso e no contexto, não apenas se existe um usuário logado.

## Erros e logging

- Retorne mensagens genéricas ao usuário: "credenciais inválidas", "não foi possível concluir a operação".
- Registre detalhes técnicos no log do servidor, com identificador de correlação.
- Nunca registre senha, token, cookie de sessão, chave privada ou dados pessoais desnecessários.
- Não use `except Exception: pass`. Trate, registre e siga com uma decisão explícita.

## Dependências e cadeia de suprimentos

- Fixe versões em `requirements.txt` ou use um lockfile.
- Rode uma ferramenta de análise de dependências (por exemplo, `pip-audit`) no CI.
- Revise dependências novas: origem, manutenção, licença e permissões.
- Não instale pacotes diretamente de URLs não verificadas em produção.
- Gere um SBOM quando o processo de release exigir rastreabilidade.

## TLS, HTTP e sessões

- Não desative a verificação de certificado (`verify=False`). Se um ambiente de laboratório exigir, isole e documente.
- Use cookies de sessão com `HttpOnly`, `Secure` e `SameSite` adequado.
- Gere identificadores de sessão com fonte criptograficamente segura e renove no login.
- Proteja operações que mudam estado contra CSRF.
- Aplique limites de taxa e bloqueio progressivo em autenticação.

## SSRF

Não permita que o usuário escolha livremente uma URL que o servidor vá buscar. Use allowlist de hosts e esquemas, bloqueie faixas privadas e metadados de nuvem, e aplique timeout e limite de resposta.

## Testes de segurança

Todo controle defensivo precisa de um teste que falharia se o controle desaparecesse:

- entrada maliciosa deve ser tratada como dado;
- usuário sem permissão deve receber negação;
- segredo não deve aparecer em log;
- caminho fora da base deve ser rejeitado;
- dependência vulnerável deve ser detectada no CI.

Testar apenas o caminho feliz não prova segurança. O teste precisa exercitar o comportamento adversário de forma controlada e local.

## Referências

- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP Top 10: https://owasp.org/Top10/
- Python Security Considerations: https://docs.python.org/3/library/security_warnings.html
- Python `hashlib`: https://docs.python.org/3/library/hashlib.html
- Python `subprocess` security considerations: https://docs.python.org/3/library/subprocess.html#security-considerations
- NIST Secure Software Development Framework: https://csrc.nist.gov/Projects/ssdf
