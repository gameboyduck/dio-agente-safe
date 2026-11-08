# Índice de evidências

Esta pasta guarda saídas reais de execução local do projeto. Nada aqui foi editado para parecer melhor do que o resultado observado.

## Ambiente da captura

- Data: 2026-11-08
- Sistema: Windows
- Python: 3.12.10
- Diretório: raiz do repositório
- Rede: não utilizada pelos testes do laboratório

## Arquivos

| Arquivo | Comando | Resultado |
|---------|---------|-----------|
| `local-test-run.txt` | `python -m unittest discover -s tests -v` | 27 testes aprovados |
| `pytest-run.txt` | `python -m pytest -q` | 27 testes e 72 subtests aprovados |
| `lab-vulnerable-output.txt` | `python examples/sql-injection/app.py` | bypass controlado retorna `True` |
| `lab-secure-output.txt` | `python examples/sql-injection/app_secure.py` | mesmo payload retorna `False` |
| `bandit-production.txt` | `python -m bandit -r . -x ./.git,./examples/sql-injection/app.py -ll` | nenhum achado |
| `bandit-fixture.txt` | `python -m bandit examples/sql-injection/app.py` | `B608`/CWE-89 esperado; saída 1 |
| `pip-audit.txt` | `python -m pip_audit -r requirements-dev.txt --strict` | nenhuma vulnerabilidade conhecida |
| `git-history.txt` | `git log --oneline --decorate` | gerado após os commits |

## O que não está aqui

- Screenshots do Hermes: pendentes.
- Transcripts de conversa com o agente: pendentes.
- Execução do GitHub Actions: pendente, pois o repositório ainda não foi publicado.
- Teste em servidor Ubuntu real: pendente e fora do escopo local.

Consulte `../evidence-guide.md` para o processo de captura e para o checklist de screenshots.

## Observações

- `bandit-fixture.txt` termina com código de saída 1 porque encontra a vulnerabilidade intencional. Isso é o comportamento correto do laboratório.
- O teste do laboratório usa banco SQLite temporário e contas sintéticas.
- Nenhuma saída contém credenciais reais ou dados pessoais.
