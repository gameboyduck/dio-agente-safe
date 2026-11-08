# Modelagem de ameaças

Modelagem de ameaças é o processo de olhar para um sistema antes de ele falhar e perguntar: o que pode dar errado, onde, por quê e o que fazemos a respeito?

Ela é mais barata do que descobrir o problema em produção e mais útil do que uma lista genérica de vulnerabilidades.

## Quando fazer

- Ao desenhar uma funcionalidade nova.
- Ao revisar uma mudança sensível (login, pagamento, upload, permissões).
- Ao integrar um serviço externo.
- Ao migrar para a nuvem.
- Ao investigar um incidente e evitar recorrência.

Não é necessário um comitê. Uma sessão de 30 a 60 minutos com quem entende o sistema já produz valor.

## Passo 1: entenda o sistema

Desenhe um diagrama simples de fluxo de dados (DFD) com:

- usuários e atores externos;
- processos da aplicação;
- armazenamentos de dados;
- serviços externos;
- fluxos de dados entre esses elementos;
- limites de confiança.

Não precisa ser bonito. Precisa ser correto.

## Passo 2: marque os limites de confiança

Um limite de confiança é onde dados ou privilégios mudam de contexto:

- navegador → servidor;
- API pública → serviço interno;
- aplicação → banco de dados;
- aplicação → shell do sistema;
- CI → produção;
- usuário comum → função administrativa;
- rede corporativa → internet.

Toda entrada que cruza um limite é não confiável até ser validada e tratada no contexto de destino.

## Passo 3: aplique STRIDE

STRIDE é um checklist de categorias de ameaça:

| Categoria | Pergunta | Exemplo |
|-----------|----------|---------|
| **S**poofing | Alguém pode se passar por outro? | Sessão previsível, senha fraca, falta de MFA |
| **T**ampering | Alguém pode alterar dados ou código? | Preço alterado no cliente, banco sem autorização |
| **R**epudiation | Alguém pode negar uma ação? | Falta de log de auditoria |
| **I**nformation disclosure | Alguém pode ver o que não deveria? | Erro com stack trace, backup público |
| **D**enial of service | Alguém pode indisponibilizar o serviço? | Consulta sem limite, upload gigante |
| **E**levation of privilege | Alguém pode ganhar mais poder? | IDOR, falha de autorização, comando injetado |

Para cada elemento do diagrama, pergunte quais categorias se aplicam.

## Passo 4: pense no atacante

Descreva o caminho de ataque em linguagem simples:

```text
Ator → ponto de entrada → ação → falha explorada → consequência
```

Exemplo:

```text
Usuário anônimo → formulário de login → envia payload SQL → consulta concatenada → login sem senha
```

Só depois mapeie para MITRE ATT&CK, se o comportamento justificar. A modelagem não precisa de ATT&CK para ser útil.

## Passo 5: avalie e priorize

Para cada ameaça, registre:

- ativo afetado;
- probabilidade;
- impacto;
- controles existentes;
- risco residual;
- dono da ação;
- prazo.

Priorize pelo risco, não pelo quanto a ameaça parece "interessante".

## Passo 6: defina controles

Prefira controles que atacam a causa:

| Ameaça | Controle fraco | Controle melhor |
|--------|----------------|-----------------|
| SQL Injection | Bloquear a palavra `OR` | Consulta parametrizada |
| XSS | Remover `<script>` | Codificação de saída por contexto |
| IDOR | Esconder o ID na URL | Verificação de autorização no recurso |
| Path traversal | Trocar `../` por vazio | Resolver caminho e validar a base |
| Força bruta | Mensagem "conta bloqueada" sem limite | Limite de tentativas e MFA |

## Exemplo: login com SQL Injection

**Fluxo:**

```text
[Usuário] --credenciais--> [Formulário] --entrada--> [Autenticação] --SQL--> [Banco]
```

**Limites de confiança:**

1. navegador → servidor;
2. aplicação → banco de dados.

**Ativos:** credenciais, contas, dados de usuários, sessão.

**Ameaças STRIDE:**

- Spoofing: login sem senha via injeção.
- Tampering: alteração de dados se a conta de banco tiver privilégios demais.
- Information disclosure: leitura de outras linhas da tabela.
- Elevation of privilege: acesso a conta administrativa.

**Controles:**

- consulta parametrizada;
- hash de senha com salt;
- conta de banco com privilégio mínimo;
- mensagem de erro genérica;
- limite de tentativas;
- log de autenticação sem senha;
- teste de regressão com payload controlado.

**Risco residual:** o laboratório continua vulnerável por design; em produção, a versão segura ainda precisa de MFA, gestão de sessão e monitoramento.

## Modelagem vs. teste

A modelagem não substitui teste, e o teste não substitui modelagem. A modelagem encontra caminhos que ninguém pensou em testar; o teste confirma ou refuta hipóteses.

## Formato de saída

```markdown
# Modelagem de ameaças: [sistema]

## Escopo e ativos
## Diagrama e limites de confiança
## Ameaças (STRIDE)
| ID | Categoria | Ameaça | Impacto | Probabilidade | Controle | Risco residual |
## Caminhos de ataque prioritários
## Premissas e limitações
## Próximos passos
```

## Limitações

- Um diagrama desatualizado produz uma modelagem errada.
- A ausência de uma ameaça na lista não prova que ela não existe.
- STRIDE é um ponto de partida, não uma auditoria completa.
- Modelagem sem acompanhamento de ações vira documentação morta.

## Referências

- OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
- OWASP Threat Dragon: https://owasp.org/www-project-threat-dragon/
- Microsoft Threat Modeling Tool: https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool
- MITRE ATT&CK: https://attack.mitre.org/
- NIST Secure Software Development Framework: https://csrc.nist.gov/Projects/ssdf
