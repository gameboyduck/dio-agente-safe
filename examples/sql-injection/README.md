# Laboratório: SQL Injection em autenticação

> ⚠️ **Código intencionalmente vulnerável.** Este laboratório existe apenas para estudo local. Não implante `app.py` em produção, não o exponha na internet e não use dados ou credenciais reais.

## Objetivo

Demonstrar, em uma aplicação Python local, como uma consulta SQL montada por interpolação permite que a entrada do usuário altere a estrutura da consulta. Depois, mostrar a correção de causa raiz com consulta parametrizada e armazenamento seguro de senha.

O laboratório é isolado:

- usa SQLite em um diretório temporário;
- usa apenas contas sintéticas;
- não acessa a rede;
- não usa dados reais;
- apaga o banco ao final da execução.

## Arquivos

| Arquivo | Papel |
|---------|-------|
| `app.py` | Versão vulnerável, com consulta SQL montada por f-string |
| `app_secure.py` | Versão corrigida, com consulta parametrizada e PBKDF2 |
| `../../tests/test_sql_injection.py` | Testes de regressão que comprovam a diferença |

## Como executar

A partir da raiz do projeto:

```bash
python examples/sql-injection/app.py
python examples/sql-injection/app_secure.py
```

Resultado esperado da versão vulnerável:

```text
1) Login com credenciais sintéticas válidas
   alice / senha-demo-123 -> True

2) Login com senha incorreta
   alice / senha-errada     -> False

3) Entrada maliciosa controlada: o texto vira parte da consulta
   usuário: ' OR '1'='1' --
   resultado -> True
```

Na versão segura, o passo 3 retorna `False`.

## A vulnerabilidade

**Nome:** SQL Injection na autenticação.

**Causa raiz:** a entrada do usuário é interpolada diretamente na string SQL:

```python
query = (
    "SELECT id FROM users "
    f"WHERE username = '{username}' AND password = '{password}'"
)
cursor.execute(query)
```

Com o usuário `' OR '1'='1' --`, a consulta se torna:

```sql
SELECT id FROM users WHERE username = '' OR '1'='1' --' AND password = '...'
```

O trecho `--` comenta o restante da consulta. A condição `OR '1'='1'` é sempre verdadeira, então a consulta retorna pelo menos uma linha e o login é aceito sem senha válida.

**Classificação:**

- OWASP Top 10: **A05:2025 Injection**.
- CWE: **CWE-89**, Improper Neutralization of Special Elements used in an SQL Command.
- CVE: não aplicável. A falha está no código didático do projeto, não em uma dependência com versão específica.
- MITRE ATT&CK: **T1190** (Exploit Public-Facing Application) só seria justificável se esta aplicação estivesse exposta na internet e a injeção fosse o vetor de acesso inicial. Neste laboratório, ela roda localmente; portanto, o mapeamento não se aplica automaticamente.

## Impacto

- **Confidencialidade:** acesso a dados de contas e a qualquer informação que a consulta possa alcançar.
- **Integridade:** dependendo do banco e das permissões, alteração ou exclusão de dados.
- **Disponibilidade:** consultas destrutivas ou custosas podem afetar o serviço.
- **Negócio:** acesso não autorizado, vazamento de dados, fraude e perda de confiança.

A severidade real depende da exposição, dos privilégios da conta de banco, dos dados armazenados e dos controles existentes. No laboratório, o risco é deliberadamente contido.

## Correção

A versão segura faz duas correções independentes:

### 1. Consulta parametrizada

```python
cursor.execute(
    "SELECT id, password_hash, salt FROM users WHERE username = ?",
    (username,),
)
```

O driver envia o valor separado da estrutura SQL. O payload continua sendo uma string, mas nunca vira comando.

### 2. Senha com hash e salt

```python
salt = secrets.token_bytes(16)
password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
```

A senha não é armazenada nem comparada em texto puro. A verificação usa `hmac.compare_digest` para evitar comparação sensível a tempo.

Para produção, prefira **Argon2id** (`argon2-cffi`) ou `scrypt`, com parâmetros calibrados e política de atualização de hash.

## Validação

Execute os testes:

```bash
python -m unittest tests.test_sql_injection -v
```

Os testes verificam:

1. a versão vulnerável contém interpolação na consulta;
2. a versão segura usa marcador de parâmetro e argumento separado;
3. o login normal continua funcionando nas duas versões;
4. a entrada maliciosa é tratada como dado na versão segura;
5. o bypass controlado ocorre apenas na versão vulnerável;
6. a senha não é armazenada em texto puro na versão segura;
7. nenhum dos arquivos importa biblioteca de rede.

Um teste de regressão só tem valor se falhar quando o controle for removido. Se alguém voltar a interpolar `username` na consulta segura, o teste de construção e o teste de bypass devem falhar.

## Limitações

- O laboratório demonstra uma falha específica; não cobre todas as formas de SQL Injection, como injeção em `ORDER BY`, nomes de tabela ou procedures.
- A versão segura é didática. Um sistema real precisa de política de senha, MFA, limitação de tentativas, proteção contra CSRF, gestão de sessão, auditoria e tratamento de erros.
- O teste de bypass é uma demonstração controlada contra um banco temporário local. Não execute o payload contra sistemas de terceiros.

## O que aprender com este laboratório

- Entrada externa nunca deve ser tratada como código.
- Parametrizar corrige a causa; filtrar caracteres apenas trata sintomas.
- Autenticação segura exige mais do que uma consulta correta: hash, salt, sessão e autorização.
- Uma correção precisa de teste que prove o comportamento adversário.
- A mesma falha tem impacto diferente conforme o contexto de exposição e os dados.

## Próximos passos

1. Explique com suas palavras por que `' OR '1'='1' --` funciona na versão vulnerável.
2. Altere o teste para incluir outro payload e verifique se a versão segura continua resistente.
3. Adicione um teste de autorização: um usuário não deve ver pedidos de outro.
4. Leia `docs/security-assessment-workflow.md` e escreva um relatório usando o modelo padronizado.
5. Rode Bandit nos dois arquivos e compare os achados.
