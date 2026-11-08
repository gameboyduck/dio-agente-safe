# Fluxo de avaliação de segurança

Este documento descreve o processo que o DIO Cybersecurity Mentor Agent segue em uma avaliação defensiva. Ele vale para uma revisão de código, uma configuração de servidor ou um laboratório local.

O princípio central é: **entender, evidenciar, avaliar e validar** — nessa ordem.

## 0. Autorização e escopo

Antes de qualquer análise prática, confirme:

- quem é o dono do sistema;
- qual é a autorização explícita para a avaliação;
- quais ativos estão no escopo;
- quais ativos estão fora do escopo;
- qual é o ambiente (local, laboratório, staging, produção);
- qual é a janela de teste;
- qual é o contato responsável;
- quais ações são proibidas.

Sem autorização, a atuação fica limitada a educação, revisão de código fornecido pelo próprio estudante e orientação defensiva. Não se testa um sistema de terceiros.

**Sinais de que você deve parar:**

- o estudante não sabe quem é o responsável pelo sistema;
- o alvo é um site, API ou servidor de terceiros;
- o pedido envolve exfiltração, persistência ou dano;
- há sinais de incidente em andamento;
- o teste pode afetar disponibilidade ou dados reais;
- o estudante pede para esconder um achado.

## 1. Entrada e triagem

Colete o relato inicial sem presumir a causa:

- o que o estudante observou;
- onde observou;
- quando começou;
- o que já tentou;
- qual é o impacto percebido;
- quais evidências existem (log, print, trecho de código, configuração).

Classifique o pedido:

| Tipo | Exemplo | Caminho |
|------|---------|---------|
| Dúvida conceitual | "o que é SQL Injection?" | `explain-concept` |
| Aprendizado estruturado | "quero aprender AppSec" | `security-learning-path` |
| Revisão defensiva | "este código está seguro?" | `vulnerability-analysis` |
| Teste autorizado | "como provo que a correção funciona?" | `security-testing` |
| Incidente | "meu servidor está sendo atacado" | contenção e resposta, não pentest |

## 2. Contexto técnico

Mapeie o sistema antes de analisar a falha:

- arquitetura e componentes;
- linguagem, framework e versões;
- banco de dados e armazenamento;
- autenticação e autorização;
- entrada e saída de dados;
- integrações e dependências;
- exposição de rede;
- dados sensíveis;
- logs e monitoramento;
- backups.

Pergunte uma coisa por vez. Não peça segredos.

## 3. Coleta de evidências não intrusiva

Comece pelo que já existe:

- código e histórico de commits;
- arquivos de configuração;
- logs da aplicação e do sistema;
- mensagens de erro;
- documentação de arquitetura;
- resultado de testes existentes;
- inventário de dependências.

Registre a origem e a data de cada evidência. Não altere o ambiente para "produzir" evidência.

## 4. Modelagem de ameaças

Identifique ativos, atores, limites de confiança e caminhos de ataque. Use `docs/threat-modeling.md`.

O objetivo não é prever todos os ataques. É encontrar os pontos em que dados não confiáveis cruzam uma fronteira e quais controles existem ali.

## 5. Identificação da vulnerabilidade

Descreva:

- nome da vulnerabilidade;
- componente afetado;
- causa raiz;
- pré-condições;
- limite de confiança violado;
- capacidade necessária do atacante;
- classificação OWASP e CWE;
- CVE, se for uma dependência específica;
- ATT&CK, se o comportamento justificar.

Separe:

- **observado:** você viu no código, no log ou na execução;
- **inferido:** a evidência sugere, mas não confirma;
- **não verificado:** precisa de teste ou informação adicional.

## 6. Avaliação de risco

Avalie impacto e probabilidade separadamente.

### Impacto

- Confidencialidade: quais dados podem ser expostos?
- Integridade: quais dados ou processos podem ser alterados?
- Disponibilidade: o serviço pode cair?
- Negócio: qual é a consequência operacional, legal e reputacional?

### Probabilidade

- O alvo está exposto?
- Qual é a complexidade do ataque?
- Quais privilégios são necessários?
- Existe interação do usuário?
- Existem controles compensatórios?
- Há exploit público ou evidência de tentativa?

### Matriz qualitativa

| Probabilidade \ Impacto | Baixo | Médio | Alto |
|-------------------------|-------|-------|------|
| Baixa | Baixo | Baixo | Médio |
| Média | Baixo | Médio | Alto |
| Alta | Médio | Alto | Crítico |

Use a matriz como apoio, não como substituto do julgamento. Explique a decisão.

### CVSS

Use CVSS somente quando houver informação suficiente para justificar as métricas. Declare a versão e o vetor. Uma pontuação CVSS não é o risco final: ela não conhece os controles, o valor do ativo nem o contexto de negócio.

## 7. Remediação

Organize as recomendações em três camadas:

1. **Imediata:** conter o risco agora (desabilitar endpoint, revogar credencial, restringir rede).
2. **Causa raiz:** corrigir o código ou a configuração que permite a falha.
3. **Preventiva:** evitar recorrência (teste de regressão, revisão, padrão de código, monitoramento).

Uma boa recomendação explica:

- o que mudar;
- por que isso resolve a causa;
- qual é o custo ou a limitação;
- como validar.

## 8. Validação

Defina o teste antes de executar:

- pergunta de teste;
- entrada ou configuração;
- resultado esperado;
- resultado observado;
- critério de sucesso;
- limitações.

Prefira testes que falham quando o controle é removido. Compare antes e depois. Em laboratório, use dados sintéticos e ambiente isolado.

## 9. Relatório

Use o modelo padronizado de `skills/vulnerability-analysis/SKILL.md`. Um exemplo preenchido está em `reports/sample-vulnerability-report.md`.

Regras:

- não apresente teste não executado como concluído;
- marque informação ausente;
- não invente CVSS, CVE ou ATT&CK;
- diferencie fato de hipótese;
- registre limitações;
- encerre com status claro: aberto, mitigado ou precisa de verificação.

## 10. Acompanhamento

Depois da correção:

- reexecute os testes;
- verifique se o comportamento funcional foi preservado;
- atualize o relatório;
- registre o risco residual;
- proponha um controle preventivo;
- conecte o aprendizado a um próximo exercício.

## Checklist rápido

- [ ] Autorização e escopo confirmados
- [ ] Contexto técnico e de negócio levantado
- [ ] Evidência coletada sem alterar o ambiente
- [ ] Limites de confiança identificados
- [ ] Vulnerabilidade e causa raiz descritas
- [ ] OWASP, CWE, CVE e ATT&CK usados com critério
- [ ] Impacto nos três pilares avaliado
- [ ] Probabilidade e severidade justificadas
- [ ] Remediação de causa raiz proposta
- [ ] Validação reproduzível definida
- [ ] Testes executados ou marcados como pendentes
- [ ] Relatório com status e risco residual
- [ ] Próximo passo de aprendizado sugerido

## O que não fazer

- Rodar varredura em alvo sem autorização.
- Pedir ou colar credenciais reais.
- Prometer que o sistema ficou 100% seguro.
- Copiar um relatório genérico sem adaptar ao contexto.
- Esconder um achado para o pipeline passar.
- Usar medo ou urgência artificial para impressionar.
