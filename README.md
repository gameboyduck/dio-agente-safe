# 🛡️ DIO Cybersecurity Mentor Agent

> Extensão do **DIO Agent** para aprender segurança de aplicações com método, evidência e prática local.

O **DIO Cybersecurity Mentor Agent** é um agente educacional que ajuda estudantes e desenvolvedores a analisar vulnerabilidades, revisar código inseguro, avaliar risco, aplicar correções e validar a remediação. Ele preserva a filosofia do DIO Agent original: ensinar a raciocinar, não entregar respostas prontas.

O projeto não treina nem modifica um modelo de linguagem. A especialização vem de instruções em Markdown, uma persona estendida, uma base de conhecimento curada, três skills, um laboratório Python e testes automatizados.

---

## 📌 Visão geral

O agente atua como mentor de cybersecurity com foco em:

- **AppSec:** revisão de código, causa raiz, impacto e remediação.
- **Desenvolvimento seguro:** padrões defensivos em Python.
- **DevSecOps:** controles automatizados no ciclo de desenvolvimento.
- **Educação:** perguntas de contexto, dicas graduais e validação reproduzível.

Ele conversa em **português do Brasil** por padrão, mantendo nomes técnicos, identificadores e frameworks no padrão internacional.

## 🎯 Motivação

Muita gente aprende segurança por listas de ferramentas e payloads. O resultado costuma ser superficial: a pessoa executa um comando, mas não entende o contexto, o impacto ou a correção.

Este projeto escolhe outro caminho:

1. entender o sistema antes de concluir;
2. separar fato de hipótese;
3. explicar a causa raiz;
4. recomendar uma correção defensável;
5. provar que a correção funciona;
6. registrar o aprendizado.

O SQL Injection foi escolhido como primeiro laboratório porque é um exemplo clássico, fácil de reproduzir localmente e rico em lições sobre entrada não confiável, banco de dados, autenticação e validação.

## 🙏 Projeto original e atribuição

Este trabalho estende o projeto oficial **[DIO Agent](https://github.com/digitalinnovationone/dio-agent)**, criado pela [DIO](https://dio.me) para acompanhar estudantes em Bootcamps, Formações, Cursos e Desafios.

- Repositório original: https://github.com/digitalinnovationone/dio-agent
- O README, o `AGENTS.md`, a persona, as skills originais e a metodologia educacional foram preservados.
- As novas funcionalidades foram adicionadas como uma especialização, sem substituir a identidade do DIO Agent.

O nome sugerido para o repositório derivado é `dio-cybersecurity-mentor-agent`.

## 🏗️ Arquitetura

```text
dio-cybersecurity-mentor-agent/
├── AGENTS.md                  Fonte única de verdade e roteamento das skills
├── README.md
├── agent/
│   ├── persona.md             Personalidade original + especialização em segurança
│   └── knowledge/
│       ├── security-basics.md
│       ├── vulnerability-classification.md
│       ├── secure-coding.md
│       └── devsecops-basics.md
├── skills/
│   ├── vulnerability-analysis/       Avaliação estruturada de vulnerabilidade
│   ├── security-testing/             Testes defensivos autorizados
│   ├── security-learning-path/       Trilha personalizada de cybersecurity
│   └── ...                           Skills originais preservadas
├── examples/sql-injection/           Laboratório vulnerável + versão segura
├── tests/                            Testes de regressão e de estrutura
├── reports/sample-vulnerability-report.md
├── docs/                             Workflow, threat modeling, evidência
├── requirements-dev.txt              Ferramentas de desenvolvimento/CI
└── .github/workflows/security-checks.yml
```

Como as peças se conectam:

1. O harness lê o `AGENTS.md` ao abrir a pasta do projeto.
2. O `AGENTS.md` define a identidade, as regras e a tabela de skills.
3. Quando a necessidade combina com uma skill, o agente abre o `SKILL.md` correspondente.
4. A skill consulta os arquivos de `agent/knowledge/` e os documentos de `docs/`.
5. O laboratório em `examples/` fornece um caso concreto.
6. Os testes em `tests/` provam o comportamento do laboratório e a integridade da configuração.
7. O workflow em `.github/workflows/` automatiza os controles no CI.

## 🧩 Skills

### Novas skills

| Skill | Para que serve | Experimente pedir |
|-------|----------------|-------------------|
| [Análise de vulnerabilidade](skills/vulnerability-analysis/SKILL.md) | Conduz uma avaliação estruturada: contexto, causa raiz, impacto, severidade, remediação, validação e relatório | "Este código de login está seguro?" |
| [Testes de segurança](skills/security-testing/SKILL.md) | Orienta testes defensivos autorizados, regressão, análise estática e dependências | "Como provo que a correção funcionou?" |
| [Trilha de cybersecurity](skills/security-learning-path/SKILL.md) | Monta um plano de estudos por nível, objetivo e tempo, com prática local | "Quero trabalhar com AppSec. Por onde começo?" |

### Skills originais preservadas

| Skill | Para que serve |
|-------|----------------|
| [Plano de estudos](skills/study-plan/SKILL.md) | Organiza o que estudar, em que ordem e em quanto tempo |
| [Destravar desafio](skills/unblock-challenge/SKILL.md) | Conduz até a solução de um desafio, sem entregar a resposta |
| [Explicar conceito](skills/explain-concept/SKILL.md) | Explica conceitos com analogias e exemplos |
| [Pesquisa na web](skills/web-search/SKILL.md) | Responde dúvidas atuais com fontes citadas |
| [Revisão de portfólio](skills/portfolio-review/SKILL.md) | Dá feedback sobre portfólio e GitHub |
| [Caminho AI Builder](skills/ai-builder-path/SKILL.md) | Ajuda a escolher o próximo passo na Carreira AI Builder |

## 📚 Base de conhecimento

| Arquivo | Conteúdo |
|---------|----------|
| [security-basics.md](agent/knowledge/security-basics.md) | Vulnerabilidade, ameaça, risco, tríade CIA, ativos, superfície de ataque, controles, privilégio mínimo |
| [vulnerability-classification.md](agent/knowledge/vulnerability-classification.md) | OWASP Top 10 2025, CWE, CVE, CVSS e MITRE ATT&CK, com o propósito de cada framework |
| [secure-coding.md](agent/knowledge/secure-coding.md) | Padrões seguros em Python: SQL, senhas, comandos, path traversal, desserialização, autorização e logs |
| [devsecops-basics.md](agent/knowledge/devsecops-basics.md) | SAST, SCA, DAST, pipeline, supply chain e segurança do próprio CI |

A base prioriza fontes reconhecidas: OWASP, MITRE, NIST, FIRST e documentação oficial do Python.

## 🚀 Como executar

### Requisitos

- Python **3.10+** (testado em Python 3.12.10).
- Nenhuma dependência de runtime: o laboratório usa apenas a biblioteca padrão.
- Git, se você for clonar o repositório.
- Hermes, se quiser usar o harness recomendado.

### 1. Obtenha o projeto

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd dio-cybersecurity-mentor-agent
```

Se estiver usando o .zip, extraia e abra a pasta que contém o `AGENTS.md`.

### 2. Rode o laboratório e os testes

```bash
python examples/sql-injection/app.py
python examples/sql-injection/app_secure.py
python -m unittest discover -s tests -v
```

### 3. Instale as ferramentas de desenvolvimento (opcional)

```bash
python -m pip install -r requirements-dev.txt
```

Isso instala Pytest, Bandit, pip-audit e PyYAML. O laboratório continua funcionando sem elas.

### 4. Rode as verificações de segurança localmente

```bash
python -m pytest -q
python -m bandit -r . -x ./.git,./examples/sql-injection/app.py -ll
python -m pip_audit -r requirements-dev.txt --strict
```

O Bandit **deve** acusar o fixture didático quando executado diretamente:

```bash
python -m bandit examples/sql-injection/app.py
```

Isso é esperado. O workflow separa esse achado para não escondê-lo e mantém os checks de produção bloqueantes.

## 🧠 Integração com Hermes

O Hermes é o harness principal do projeto. A documentação oficial está em https://hermes-agent.nousresearch.com/docs.

1. Instale o Hermes seguindo a documentação oficial do seu sistema.
2. Abra o terminal **na raiz do repositório**, onde está o `AGENTS.md`.
3. Inicie:

   ```bash
   hermes
   ```

4. Confira se o contexto foi carregado com `/context`. O `AGENTS.md` do projeto deve aparecer.
5. Pergunte algo como:

   ```text
   Tenho um servidor Ubuntu exposto na internet. Como sei se está vulnerável?
   ```

O `AGENTS.md` é lido a partir do diretório de trabalho. As skills deste projeto ficam em `skills/` e são registradas no `AGENTS.md`; o agente as abre pelo caminho indicado quando a conversa combina com o processo. O Hermes também possui descoberta nativa de skills em `.hermes/skills/` e `.agents/skills/`; este repositório mantém a convenção original da DIO, baseada no `AGENTS.md`, para funcionar em vários harnesses.

> **Status:** a integração foi documentada com base na documentação oficial, mas **não foi executada neste ambiente**. Não há credenciais de modelo configuradas. Veja `tests/test_agent_behavior.md` e `docs/evidence-guide.md`.

## 🧪 Demonstração prática: SQL Injection

O laboratório `examples/sql-injection/` tem duas versões:

- `app.py`: intencionalmente vulnerável, com consulta SQL montada por f-string.
- `app_secure.py`: consulta parametrizada e senha com PBKDF2 + salt.

### Antes

```python
query = (
    "SELECT id FROM users "
    f"WHERE username = '{username}' AND password = '{password}'"
)
cursor = connection.execute(query)
```

Com o usuário `' OR '1'='1' --`, a consulta vira:

```sql
SELECT id FROM users WHERE username = '' OR '1'='1' --' AND password = '...'
```

O login é aceito sem senha válida.

### Depois

```python
cursor = connection.execute(
    "SELECT id, password_hash, salt FROM users WHERE username = ?",
    (username,),
)
```

O payload é tratado como dado. A verificação de senha usa `hmac.compare_digest` sobre o hash.

### Resultado observado

| Cenário | `app.py` | `app_secure.py` |
|---------|----------|-----------------|
| `alice / senha-demo-123` | `True` | `True` |
| `alice / senha-errada` | `False` | `False` |
| `' OR '1'='1' -- / qualquer-coisa` | `True` (bypass intencional) | `False` |
| Senha em texto puro no banco | Sim (intencional) | Não |

A análise completa está em [reports/sample-vulnerability-report.md](reports/sample-vulnerability-report.md). O passo a passo está em [examples/sql-injection/README.md](examples/sql-injection/README.md).

## 🖥️ Cenário: servidor Ubuntu exposto

O documento [docs/ubuntu-server-security.md](docs/ubuntu-server-security.md) mostra como o agente deveria conduzir o pedido "tenho um servidor Ubuntu exposto, ele está vulnerável?". O roteiro começa por autorização, escopo e exposição, antes de qualquer comando, e depois propõe verificações read-only.

> **Status:** o roteiro está documentado e revisado. Ele **não foi executado** em um servidor Ubuntu real, e não há transcript do agente no Hermes.

## 📊 Classificação de risco

O agente usa quatro níveis qualitativos: **Baixa**, **Média**, **Alta** e **Crítica**.

A avaliação considera:

- impacto em confidencialidade, integridade e disponibilidade;
- impacto operacional e de negócio;
- exposição do alvo;
- privilégios e complexidade necessários;
- controles existentes;
- probabilidade de exploração.

Quando há informação suficiente, o agente pode usar **CVSS** (v3.1 ou v4.0), declarando a versão e o vetor. Ele não copia pontuação de outra fonte e não trata CVSS como risco de negócio. Também não mapeia automaticamente toda falha para MITRE ATT&CK.

A distinção é explícita:

- **severidade estimada:** qualitativa, baseada no contexto;
- **CVSS calculado:** métricas declaradas e justificadas;
- **risco:** combinação de probabilidade, impacto e contexto.

## 🔁 DevSecOps

O workflow [`.github/workflows/security-checks.yml`](.github/workflows/security-checks.yml) roda em pull requests e pushes para `main`. Ele tem quatro jobs:

| Job | O que faz |
|-----|-----------|
| **Code quality** | Valida sintaxe Python e executa os testes automatizados |
| **Dependency security** | Audita as dependências de desenvolvimento com pip-audit |
| **Static security** | Roda Bandit; falha em achados relevantes fora do fixture didático |
| **Agent configuration** | Valida frontmatter, registro das skills, caminhos, conhecimento e YAML |

Controles aplicados:

- permissões de workflow restritas a `contents: read`;
- checkout sem persistência de credenciais;
- ações oficiais em versões mantidas (recomenda-se fixar por SHA em ambientes que exijam referência imutável);
- nenhum segredo em log;
- exceção estreita e explícita para `examples/sql-injection/app.py`;
- achado didático exibido em passo separado, não ocultado;
- checks de produção continuam bloqueantes.

> **Status:** o workflow foi criado e validado sintaticamente neste ambiente, mas **não foi executado no GitHub Actions**, porque o repositório ainda não foi publicado.

## 📸 Evidências

O guia completo está em [docs/evidence-guide.md](docs/evidence-guide.md). A pasta `docs/evidence/` contém apenas saídas reais de execução local.

| Evidência | Status |
|-----------|--------|
| Testes locais | Executado — veja `docs/evidence/local-test-run.txt` |
| Demonstração do laboratório | Executado — veja `docs/evidence/` |
| Bandit | Executado — veja `docs/evidence/` |
| pip-audit | Executado — veja `docs/evidence/` |
| Hermes em execução | Pendente — requer modelo configurado |
| Screenshots do agente | Pendente — não foram fabricados |
| GitHub Actions | Pendente — repositório não publicado |

Nenhum screenshot, transcript ou resultado foi inventado. Se uma evidência não existe, ela é marcada como pendente.

## 🔒 Segurança e ética

- Pratique apenas em sistemas próprios ou com autorização explícita.
- Não use o laboratório contra sistemas de terceiros.
- Não insira dados reais nem credenciais no laboratório.
- Não implante `examples/sql-injection/app.py`.
- Não peça, cole ou reproduza segredos.
- Não use os testes para exfiltrar dados, persistir ou causar dano.
- Relate achados com evidência, contexto e limitações.

O projeto é educacional. Ele não substitui um pentest profissional, um programa de segurança ou uma avaliação jurídica.

## 🗂️ Estrutura detalhada

```text
.
├── AGENTS.md
├── README.md
├── CLAUDE.md
├── requirements-dev.txt
├── agent/
│   ├── persona.md
│   └── knowledge/
│       ├── dio-platform.md
│       ├── learning-experiences.md
│       ├── security-basics.md
│       ├── vulnerability-classification.md
│       ├── secure-coding.md
│       └── devsecops-basics.md
├── skills/
│   ├── README.md
│   ├── study-plan/
│   ├── unblock-challenge/
│   ├── explain-concept/
│   ├── web-search/
│   ├── portfolio-review/
│   ├── ai-builder-path/
│   ├── vulnerability-analysis/
│   ├── security-testing/
│   └── security-learning-path/
├── examples/
│   └── sql-injection/
│       ├── app.py
│       ├── app_secure.py
│       └── README.md
├── tests/
│   ├── test_sql_injection.py
│   ├── test_skill_structure.py
│   └── test_agent_behavior.md
├── reports/
│   └── sample-vulnerability-report.md
├── docs/
│   ├── glossary.md
│   ├── youcom-mcp.md
│   ├── security-assessment-workflow.md
│   ├── threat-modeling.md
│   ├── evidence-guide.md
│   ├── ubuntu-server-security.md
│   └── evidence/
└── .github/
    └── workflows/
        └── security-checks.yml
```

## ✅ Resultados e limitações

### Implementado

- Persona estendida, sem substituir a identidade original.
- `AGENTS.md` com as três novas skills e os quatro arquivos de conhecimento.
- Base de conhecimento de segurança.
- Skills de análise, testes e trilha de aprendizado.
- Laboratório de SQL Injection com versão vulnerável e segura.
- Testes de regressão e de estrutura.
- Relatório padronizado de exemplo.
- Documentação de workflow, threat modeling e evidências.
- Workflow de CI com análise estática, dependências e validação do agente.

### Testado e verificado localmente

- 27 testes automatizados aprovados: 11 do laboratório e 16 de estrutura e configuração.
- Testes de estrutura aprovados (skills, frontmatter, caminhos, relatório, YAML).
- Bandit: achado `B608`/CWE-89 no fixture e nenhum achado no código seguro.
- pip-audit: nenhuma vulnerabilidade conhecida nas dependências de desenvolvimento.
- Demonstrações locais das duas versões executadas.

### Não testado ou pendente

- Execução real no Hermes com um modelo configurado.
- Testes comportamentais do agente (CT-01 a CT-09).
- Execução do workflow no GitHub Actions.
- Screenshots e transcripts de uma sessão real.
- Publicação do repositório no GitHub.
- Teste em infraestrutura Ubuntu real ou simulada.

### Limitações técnicas

- O laboratório cobre uma forma de SQL Injection, não todas.
- A versão segura é didática; não é um sistema de autenticação completo.
- O relatório de exemplo é uma avaliação de laboratório, não de produção.
- Bandit e pip-audit não provam ausência de vulnerabilidades.
- O agente depende do modelo e do harness; instruções reduzem variabilidade, mas não a eliminam.

## 🚧 Próximos passos

- Executar os cenários de `tests/test_agent_behavior.md` no Hermes e registrar transcripts reais.
- Publicar o repositório e validar o workflow no GitHub Actions.
- Adicionar laboratórios de XSS, IDOR, path traversal e command injection.
- Integrar Semgrep com regras específicas do projeto.
- Gerar SBOM e verificar proveniência de artefatos.
- Adicionar teste de autorização entre usuários.
- Criar um exemplo de modelagem de ameaças com diagrama.
- Avaliar a descoberta nativa de skills do Hermes via `.hermes/skills/` ou `external_dirs`, sem quebrar a compatibilidade com outros harnesses.

## 🤝 Contribuição

Contribuições são bem-vindas. Leia [skills/README.md](skills/README.md) antes de criar uma skill.

Regras:

- preserve a identidade e a metodologia do DIO Agent;
- mantenha o foco educativo;
- não inclua dados reais ou segredos;
- adicione testes para qualquer correção de segurança;
- documente limitações e evidências;
- não esconda achados de segurança.

## 🙌 Créditos

- Projeto original: [DIO Agent](https://github.com/digitalinnovationone/dio-agent), da [DIO](https://dio.me).
- Frameworks e referências: OWASP, MITRE, NIST, FIRST e documentação oficial do Python.
- Este projeto é uma especialização educacional independente, construída sobre a arquitetura e a filosofia do DIO Agent.

---

**Segurança se aprende com contexto, prática e evidência. Não com medo e não com atalhos.**
