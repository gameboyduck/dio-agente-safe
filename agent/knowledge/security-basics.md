# Fundamentos de segurança

Este arquivo reúne os conceitos que o agente precisa dominar antes de analisar qualquer cenário de segurança. O objetivo é explicar com precisão, sem transformar a conversa em um glossário decorado.

## Vulnerabilidade, ameaça e risco

Os três termos são diferentes e não devem ser usados como sinônimos.

**Vulnerabilidade** é uma fraqueza que pode ser explorada para comprometer um sistema ou um objetivo de segurança. É uma característica do próprio sistema: código, configuração, processo ou dependência.

- Exemplo: uma consulta SQL montada por concatenação de texto com a entrada do usuário.
- Exemplo: um bucket de armazenamento com leitura pública.
- Exemplo: uma senha administrativa compartilhada em um arquivo de configuração.

**Ameaça** é uma causa potencial de um evento de segurança indesejado. Pode ser uma pessoa, um grupo, um programa ou um evento natural.

- Exemplo: um atacante que procura aplicações expostas na internet.
- Exemplo: um funcionário que clica em um link de phishing.
- Exemplo: uma falha de energia que derruba o servidor.

**Risco** é a possibilidade de perda ou dano, considerando a probabilidade de uma ameaça explorar uma vulnerabilidade e as consequências disso.

- Exemplo: uma falha de SQL Injection em um sistema interno, sem dados sensíveis e com acesso restrito, tende a ter risco menor do que a mesma falha em um portal público de autenticação.
- Exemplo: uma dependência desatualizada sem caminho de exploração conhecido no contexto ainda é um risco, mas a severidade não deve ser inflada sem evidência.

Uma forma útil de pensar:

```text
Risco ≈ probabilidade de exploração × impacto
```

A fórmula não substitui uma avaliação estruturada. Ela só lembra que severidade técnica e risco de negócio não são a mesma coisa.

## Tríade CIA

A tríade CIA resume os três objetivos clássicos de segurança da informação.

### Confidencialidade

Garante que a informação seja acessível apenas a quem tem autorização.

- Exemplos de falha: dados pessoais retornados para outro usuário, backup sem criptografia, log com senha em texto puro.
- Controles típicos: autenticação, autorização, criptografia em trânsito e em repouso, segregação de dados, minimização de privilégios.

### Integridade

Garante que os dados não sejam alterados de forma não autorizada e que a origem da informação possa ser verificada.

- Exemplos de falha: um usuário comum consegue alterar o preço de um produto, um atacante modifica um registro de auditoria, um download é corrompido sem detecção.
- Controles típicos: validação de entrada, controles de autorização, assinaturas digitais, checksums, trilhas de auditoria, transações.

### Disponibilidade

Garante que usuários autorizados consigam acessar sistemas e informações quando precisarem.

- Exemplos de falha: um ataque de negação de serviço, uma consulta sem limite que derruba o banco, um disco sem redundância.
- Controles típicos: redundância, limites de taxa, backups testados, monitoramento, capacidade planejada, proteção contra DDoS.

Uma falha pode afetar mais de um pilar. SQL Injection em uma tela de login, por exemplo, pode permitir acesso não autorizado (confidencialidade e integridade) e, dependendo do payload, alteração ou destruição de dados (integridade e disponibilidade).

## Conceitos de arquitetura e ataque

**Ativo** é algo que tem valor para a organização: dados, credenciais, serviços, reputação, processos de negócio, infraestrutura.

**Superfície de ataque** é o conjunto de pontos pelos quais um atacante pode tentar interagir com o sistema. Inclui APIs, formulários, portas abertas, painéis administrativos, dependências, contas de usuário e até processos humanos.

**Vetor de ataque** é o caminho concreto usado para explorar uma vulnerabilidade. Por exemplo: um formulário de login público que envia entrada não validada para uma consulta SQL.

**Ator de ameaça** é quem ou o que pode causar o evento: atacante externo, insider, grupo criminoso, pesquisador, script automatizado ou erro humano.

**Limite de confiança** (trust boundary) é a fronteira onde dados ou privilégios mudam de contexto. Exemplos: navegador para servidor, aplicação para banco de dados, rede pública para rede interna, serviço A para serviço B. A maioria das vulnerabilidades exploráveis envolve cruzar um limite de confiança com dados não confiáveis.

## Controles de segurança

**Controle** é uma medida que reduz risco. Os tipos mais usados:

- **Preventivo:** impede que o evento ocorra. Exemplo: consulta parametrizada, firewall, MFA.
- **Detectivo:** identifica que algo ocorreu. Exemplo: log de auditoria, alerta de acesso anômalo, IDS.
- **Corretivo:** reduz o impacto depois do evento. Exemplo: backup restaurável, rotação de credenciais, isolamento de host comprometido.
- **Compensatório:** alternativa quando o controle ideal não é viável. Exemplo: monitoramento intensivo no lugar de uma correção que depende de um fornecedor.

**Defesa em profundidade** significa combinar controles em camadas, para que a falha de uma não deixe o sistema totalmente exposto. Exemplo: validação de entrada, consulta parametrizada, usuário de banco com privilégio mínimo e monitoramento de erros.

**Privilégio mínimo** significa conceder apenas as permissões necessárias para a tarefa, pelo tempo necessário. Vale para pessoas, serviços, contas de banco, tokens de CI e processos.

## Autenticação e autorização

**Autenticação** responde "quem é você?". Envolve senha, chave, biometria, MFA, passkeys ou outro fator.

**Autorização** responde "o que você pode fazer?". Envolve papéis, permissões, políticas e verificações por recurso.

Confundir as duas é um erro comum. Um usuário autenticado não deve, por isso, ter acesso a qualquer recurso. Falhas de autorização são uma das categorias mais frequentes em aplicações web.

## Validação de entrada e codificação de saída

**Validação de entrada** verifica se o dado recebido tem o formato, o tamanho e os valores esperados. Prefira listas de permissão (allowlist) a listas de bloqueio (denylist).

**Codificação de saída** garante que o dado seja interpretado como dado no contexto de destino: HTML, SQL, shell, JSON, cabeçalho HTTP. Cada contexto exige uma codificação diferente.

A regra prática é: valide na entrada quando possível, mas trate todo dado externo como não confiável até o ponto de uso. Nunca presuma que uma validação feita em outro lugar continua válida.

## Desenvolvimento seguro e monitoramento

**Desenvolvimento seguro de software** é integrar segurança ao ciclo de vida: requisitos, modelagem de ameaças, revisão de código, testes, análise estática, gestão de dependências e resposta a incidentes.

**Monitoramento e logging de segurança** permitem detectar, investigar e responder. Logs úteis respondem quem, o quê, quando, onde e resultado, sem registrar segredos ou dados pessoais desnecessários. Log sem alerta e sem revisão tem valor limitado.

## Como usar estes conceitos em uma análise

1. Identifique o ativo e o objetivo de segurança afetado.
2. Descreva a vulnerabilidade e o limite de confiança violado.
3. Separe o que foi observado do que é hipótese.
4. Avalie impacto nos três pilares e no negócio.
5. Estime probabilidade e severidade com evidência.
6. Recomende controles que ataquem a causa, não apenas o sintoma.
7. Defina como validar a correção.

## Referências

- OWASP Top 10: https://owasp.org/Top10/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
- MITRE CWE: https://cwe.mitre.org/
- MITRE ATT&CK: https://attack.mitre.org/
- FIRST CVSS: https://www.first.org/cvss/
