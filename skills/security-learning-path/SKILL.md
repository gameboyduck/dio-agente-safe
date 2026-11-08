---
name: security-learning-path
description: Use quando o estudante quer aprender segurança da informação ou montar um plano de estudos de cybersecurity. Personaliza a trilha por nível, objetivo e tempo disponível, com exercícios práticos em ambientes locais ou intencionalmente vulneráveis.
---

# Skill: Trilha de aprendizado em cybersecurity

Monta um plano de estudos personalizado para quem quer entrar ou evoluir em segurança, partindo do nível real do estudante e de um objetivo concreto. O plano combina fundamentos, prática defensiva e projetos de portfólio.

## Quando usar

Use esta skill quando o estudante:

- quer começar em cybersecurity e não sabe por onde;
- quer se especializar em AppSec, DevSecOps, blue team ou segurança de nuvem;
- pede um cronograma de estudos na área;
- quer praticar com laboratórios;
- quer escolher o próximo tema depois de aprender o básico.

Para um plano focado em uma experiência específica da DIO, combine com `study-plan`. Para entender um conceito pontual, use `explain-concept`.

## Processo

### 1. Entenda o ponto de partida

Pergunte, uma coisa por vez:

- Qual é o objetivo? (primeiro emprego, transição de carreira, evoluir na função atual, certificação, projeto pessoal)
- Qual é o nível atual? (nunca estudou, sabe programar, já trabalha com TI, já trabalha com segurança)
- Quanto tempo por dia ou por semana consegue dedicar?
- Existe prazo?
- Qual é a base de programação, redes e Linux?
- Já tem um ambiente para praticar?

Não presuma que "segurança" significa a mesma coisa para todo mundo. Pentest, AppSec, DevSecOps, resposta a incidentes e segurança de nuvem são caminhos diferentes.

### 2. Escolha o foco

Ajude o estudante a escolher uma direção principal. É melhor uma trilha coerente do que um mosaico de temas avançados sem base.

| Foco | Combina com quem gosta de | Base necessária |
|------|---------------------------|-----------------|
| Fundamentos e blue team | Investigar, monitorar, responder | Redes, Linux, logs |
| AppSec | Ler e escrever código, revisar aplicações | Programação, HTTP, banco de dados |
| DevSecOps | Automatizar, operar pipelines, infraestrutura | Git, CI/CD, containers, cloud |
| Pentest autorizado | Testar sistemas com método | Redes, Linux, web, relatórios |
| Segurança de nuvem | Configuração, identidade, arquitetura | Cloud, IAM, redes |

### 3. Monte a trilha por módulos

Use os módulos abaixo como blocos. Não é obrigatório fazer todos, mas a ordem ajuda. Ajuste a profundidade ao objetivo.

| # | Módulo | O que estudar | Prática sugerida |
|---|--------|---------------|------------------|
| 1 | Fundamentos de cybersecurity | Vocabulário, ameaça, vulnerabilidade, risco, controles | Analisar um incidente público e identificar ativo, ameaça, vulnerabilidade e impacto |
| 2 | Tríade CIA e princípios | Confidencialidade, integridade, disponibilidade, defesa em profundidade, privilégio mínimo | Classificar um incidente fictício nos três pilares |
| 3 | Redes e Linux | TCP/IP, HTTP, DNS, portas, permissões, processos, logs | Inspecionar sua própria máquina Linux ou uma VM local |
| 4 | Segurança de aplicações web | HTTP, sessão, cookies, autenticação, autorização, entrada | Mapear um fluxo de login local com diagrama de confiança |
| 5 | OWASP Top 10 | Categorias de risco e exemplos | Relacionar cada categoria a um exemplo de código |
| 6 | Desenvolvimento seguro em Python | Validação, parametrização, hashing, segredos, erros | Corrigir o laboratório `examples/sql-injection/` |
| 7 | Autenticação e controle de acesso | Senhas, MFA, sessão, autorização por recurso | Testar acesso indevido entre dois usuários sintéticos |
| 8 | Modelagem de ameaças | Limites de confiança, STRIDE, árvores de ataque | Modelar um sistema simples de login |
| 9 | Gestão de vulnerabilidades | CVE, CWE, CVSS, priorização, ciclo de correção | Classificar achados de um projeto próprio |
| 10 | Testes de segurança | Testes de regressão, SAST, SCA, DAST autorizado | Rodar `unittest` e Bandit no laboratório |
| 11 | Fundamentos de cloud | IAM, redes, storage, logs, responsabilidade compartilhada | Revisar uma configuração de exemplo, sem aplicar em produção |
| 12 | DevSecOps e CI/CD | Pipeline, segredos, permissões, supply chain | Ler o workflow `.github/workflows/security-checks.yml` |
| 13 | Monitoramento e resposta | Logs, alertas, triagem, contenção, evidências | Escrever um plano de resposta para um incidente fictício |
| 14 | Projeto de portfólio | Documentação, reprodutibilidade, ética | Publicar um laboratório com README, testes e relatório |

### 4. Distribua no tempo

Calcule a carga a partir do tempo real do estudante. Um plano de 6 horas por semana é mais sustentável do que um de 20 horas que dura duas semanas.

Exemplo de estrutura para 8 semanas, 6 horas por semana, foco em AppSec:

- Semanas 1–2: módulos 1 a 4, com prática de HTTP, CIA e Linux.
- Semanas 3–4: módulos 5 e 6, corrigindo o laboratório de SQL Injection.
- Semana 5: módulo 7, com testes de autorização.
- Semana 6: módulo 8, modelagem de ameaças de um projeto próprio.
- Semana 7: módulos 9 e 10, relatório e testes automatizados.
- Semana 8: módulo 14, organizando o portfólio e revisando a documentação.

Inclua dias de revisão e um buffer. Imprevistos acontecem.

### 5. Defina marcos verificáveis

Um marco precisa ser observável, não uma sensação:

- "Explico a diferença entre vulnerabilidade, ameaça e risco com um exemplo próprio."
- "Consigo identificar uma consulta SQL insegura e reescrevê-la com parâmetros."
- "Meu teste de regressão falha se eu remover a parametrização."
- "Produzi um relatório com evidência, impacto e limitações."
- "Meu laboratório roda localmente sem dados reais."

### 6. Conecte com a DIO sem inventar

Use as experiências reais da DIO descritas em `agent/knowledge/learning-experiences.md` (Bootcamps, Formações, Acelerações, Cursos, Desafios, Lives e Mentorias). Não invente nomes, datas ou trilhas de segurança. Se não houver confirmação de um curso específico, oriente o estudante a procurar na plataforma pelo tema e ofereça a trilha genérica.

Um Desafio de Projeto pode virar um excelente item de portfólio: aplicação local, README, teste e relatório de segurança.

### 7. Entregue o plano

Inclua:

- objetivo e nível;
- foco escolhido;
- módulos em ordem, com tempo estimado;
- prática de cada módulo;
- marcos;
- projeto final;
- o que fica fora do escopo nesta etapa;
- como revisar o progresso.

Pergunte se o ritmo é possível e ajuste.

## Regras de segurança e ética

- Toda prática deve ocorrer em ambiente próprio, local ou explicitamente autorizado.
- Use aplicações intencionalmente vulneráveis apenas em laboratório isolado.
- Não aponte ferramentas para sites de terceiros.
- Não ensine a invadir, persistir ou exfiltrar dados.
- Explique a diferença entre aprender segurança e prestar serviço profissional regulamentado.
- Reforce que relatório, escopo e autorização fazem parte da competência.

## Formato de saída

```markdown
# Plano de estudos em cybersecurity

## Objetivo e ponto de partida
## Foco escolhido
## Trilha por módulos
| Semana | Módulo | Estudo | Prática | Marco |
## Projeto final
## Rotina e revisão
## Limites e próximos passos
```

## Lembre-se

- Segurança se aprende praticando, mas prática sem ética é risco.
- Fundamentos de redes, Linux e programação aceleram qualquer especialização.
- Um projeto bem documentado vale mais que dez certificados sem evidência.
- O plano precisa caber na vida real do estudante.

## Referências

- `agent/knowledge/security-basics.md`
- `agent/knowledge/vulnerability-classification.md`
- `agent/knowledge/secure-coding.md`
- `agent/knowledge/devsecops-basics.md`
- `docs/security-assessment-workflow.md`
- `docs/threat-modeling.md`
- `examples/sql-injection/README.md`
