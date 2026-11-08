# Testes de segurança

Skill de testes defensivos autorizados. Ela transforma uma hipótese de segurança em um teste reproduzível, com escopo, evidência e limitações declaradas.

## O que a skill faz

- Exige autorização e escopo antes de executar qualquer teste.
- Orienta revisão de código, testes de regressão, verificação de configuração e análise de dependências.
- Apresenta ferramentas adequadas sem executar tudo automaticamente.
- Documenta o que foi e o que não foi testado.
- Ensina a comparar a postura antes e depois da correção.

## Quando a skill é selecionada

O estudante quer testar uma correção, rodar análise estática, verificar autenticação/autorização ou praticar em laboratório local.

## Ferramentas citadas

- Python `unittest` e Pytest.
- Bandit.
- pip-audit.
- Semgrep.
- OWASP ZAP, apenas em ambiente autorizado.

## Exemplo de pedido

> "Corrigi a consulta SQL. Como provo que o bypass não funciona mais?"

O comportamento esperado é definir um teste de regressão com banco temporário, executar antes e depois e registrar o resultado, sem testar nenhum sistema externo.

## Arquivos relacionados

- `SKILL.md`: processo, portão de autorização e formato de saída.
- `../../examples/sql-injection/README.md`: laboratório local.
- `../../tests/test_sql_injection.py`: testes de regressão executáveis.
- `../../docs/evidence-guide.md`: como registrar evidências.

## Limites

A skill não substitui um pentest profissional, não cobre todos os tipos de falha e não autoriza testes em sistemas de terceiros. Resultado de ferramenta não é prova de segurança.
