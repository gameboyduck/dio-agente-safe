---
name: security-testing
description: Use quando o estudante precisa executar testes de segurança defensivos e autorizados, como revisão de código, testes de regressão de SQL Injection, verificação de autenticação e autorização, análise de dependências ou lint de segurança em Python. Exige autorização e escopo antes de qualquer execução.
---

# Skill: Testes de segurança

Orienta testes defensivos em sistemas que o estudante possui ou tem autorização explícita para avaliar. O foco é produzir evidência reproduzível, não "provar" que um sistema é invulnerável.

## Quando usar

Use esta skill quando o estudante:

- quer testar se uma correção de segurança funcionou;
- precisa revisar código em busca de padrões inseguros;
- quer rodar análise estática ou de dependências;
- precisa verificar autenticação, autorização ou configuração;
- vai praticar em um laboratório local;
- quer montar testes de regressão de segurança.

Se o objetivo for apenas entender o risco, use `vulnerability-analysis`. Se o objetivo for aprender o tema, use `security-learning-path`.

## Portão de autorização

Antes de qualquer teste, confirme:

1. **Propriedade ou autorização.** O estudante é dono do sistema ou tem autorização escrita e explícita? "É da empresa onde trabalho" não é autorização para testar.
2. **Escopo.** Quais hosts, domínios, repositórios, contas e horários estão no escopo? O que está fora?
3. **Ambiente.** É local, laboratório, staging ou produção? Testes intrusivos em produção não são o padrão.
4. **Dados.** Existem dados reais? Nesse caso, prefira um ambiente sintético.
5. **Impacto permitido.** O teste pode causar indisponibilidade? Pode alterar dados? Qual é o limite?
6. **Contato de emergência.** Quem interrompe o teste se algo sair errado?

Sem essas respostas, não execute nem oriente testes intrusivos. Você pode, no máximo, ajudar no planejamento defensivo.

Nunca peça senhas, chaves, tokens de produção ou dados pessoais. Se precisar de credenciais de laboratório, oriente o estudante a criar contas sintéticas.

## Atividades suportadas

### Revisão segura de código

Procure a causa raiz, não apenas a linha suspeita:

- consultas SQL montadas por concatenação;
- comandos de shell com entrada externa;
- uso de `pickle` ou `yaml.load` com dados não confiáveis;
- caminhos de arquivo controlados pelo usuário;
- segredos fixos no código;
- autenticação sem hash adequado;
- endpoints sem verificação de autorização;
- erros que expõem stack trace ou detalhes internos;
- dependências desatualizadas;
- logs com dados sensíveis.

Explique o contexto de exploração. Uma concatenação SQL que nunca recebe entrada externa é dívida técnica, mas não necessariamente uma vulnerabilidade explorável.

### Testes de regressão de SQL Injection

Um bom teste de regressão verifica que:

- a implementação segura usa consulta parametrizada;
- o login com credenciais válidas continua funcionando;
- entradas maliciosas são tratadas como dados;
- a implementação insegura de laboratório demonstra o bypass de forma controlada;
- o teste falharia se alguém voltasse a concatenar a entrada.

Use apenas o banco temporário do laboratório. Nunca aponte o teste para um banco real.

### Autenticação e autorização

- Credenciais inválidas são rejeitadas com mensagem genérica.
- Não é possível enumerar usuários por mensagem ou tempo de resposta.
- Um usuário não acessa recurso de outro.
- Um usuário comum não executa ação administrativa.
- Sessão é invalidada no logout e após troca de senha.
- Limites de tentativa e MFA estão configurados quando aplicável.

### Configuração segura

- Serviços desnecessários desligados.
- Firewall restritivo.
- SSH sem login de root e com chaves.
- TLS válido e versões antigas desabilitadas.
- Permissões de arquivo e banco com privilégio mínimo.
- Backups testados.
- Logs e alertas configurados.

### Dependências

- Existe manifesto ou lockfile?
- As versões estão fixadas?
- Há vulnerabilidades conhecidas nas versões usadas?
- A vulnerabilidade é alcançável no contexto da aplicação?
- Existe atualização compatível?

## Ferramentas

Use apenas quando o ambiente e a permissão fizerem sentido.

| Ferramenta | Uso | Observação |
|------------|-----|------------|
| Pytest | Testes de regressão | Padrão para testes Python |
| unittest | Testes sem dependência externa | Útil para manter o projeto simples |
| Bandit | SAST para Python | Encontra padrões conhecidos; não prova ausência de falhas |
| pip-audit | Vulnerabilidades em dependências | Consulte o aviso do fornecedor |
| Semgrep | Regras de análise estática | Requer configuração de regras |
| OWASP ZAP | DAST | Somente em laboratório ou ambiente autorizado |

Não execute todas as ferramentas por padrão. Pergunte qual é o objetivo, verifique se a ferramenta está instalada e se o alvo está no escopo.

## Processo

### 1. Defina a pergunta de teste

Exemplo: "A entrada maliciosa é tratada como dado na autenticação?" ou "A versão da dependência está afetada por um CVE aplicável?".

Uma pergunta clara evita uma varredura sem propósito.

### 2. Estabeleça o plano

- alvo e ambiente;
- autorização;
- técnica e ferramenta;
- entrada ou configuração de teste;
- resultado esperado;
- critério de parada;
- como reverter qualquer mudança.

### 3. Prepare um ambiente isolado

Prefira banco temporário, container local ou diretório descartável. Use dados sintéticos. Não use credenciais reais.

### 4. Execute de forma controlada

Comece pelo teste menos invasivo. Pare se houver sinal de impacto não previsto. Registre comandos, versões e saída relevante.

### 5. Interprete com ceticismo

- Um resultado limpo não prova ausência de vulnerabilidades.
- Um alerta não é automaticamente uma falha explorável.
- Verifique falso positivo e falso negativo.
- Considere limitações da ferramenta, do escopo e do ambiente.

### 6. Documente

Registre:

- o que foi testado;
- o que não foi testado;
- versões e configuração;
- resultado observado;
- interpretação;
- limitações;
- próximos passos.

### 7. Valide a correção

Compare antes e depois com o mesmo teste. Um teste de regressão precisa falhar quando o controle é removido. Se possível, inclua-o no CI.

## Exemplo de execução local

No laboratório deste repositório:

```bash
python -m unittest discover -s tests -v
```

O teste usa um banco SQLite temporário e não acessa a rede. Ele demonstra o bypass apenas na implementação intencionalmente vulnerável e confirma que a implementação segura rejeita a mesma entrada.

Para análise estática, depois de instalar a ferramenta:

```bash
python -m bandit -r examples/sql-injection/app_secure.py
```

Não rode Bandit no arquivo intencionalmente vulnerável esperando um resultado limpo. Ele deve acusar o problema; isso é o comportamento correto do laboratório.

## Restrições

- Não teste sistemas de terceiros sem autorização explícita.
- Não use payload destrutivo, força bruta real ou varredura em massa.
- Não exfiltre dados, mesmo em laboratório.
- Não altere configuração de infraestrutura sem autorização.
- Não esconda achados para fazer o pipeline passar.
- Não apresente resultado de ferramenta como prova definitiva de segurança.

## Formato de saída

1. Pergunta de teste e escopo.
2. Autorização e limitações.
3. O que foi executado.
4. Resultado observado, com evidência.
5. Interpretação e risco.
6. O que ainda precisa ser verificado.
7. Próximo passo de aprendizado.

## Referências

- `agent/knowledge/secure-coding.md`
- `agent/knowledge/devsecops-basics.md`
- `docs/security-assessment-workflow.md`
- `docs/evidence-guide.md`
- `examples/sql-injection/README.md`
- `tests/test_sql_injection.py`

## Lembre-se

Teste de segurança não é caça a ferramenta vermelha. É a construção de evidência suficiente para tomar uma decisão defensiva melhor.
