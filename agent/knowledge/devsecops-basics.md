# Fundamentos de DevSecOps

DevSecOps é a prática de integrar segurança ao desenvolvimento e à operação, de forma contínua, automatizada e proporcional ao risco. A ideia não é adicionar uma etapa burocrática no fim do processo, e sim tornar a decisão segura parte do fluxo normal de quem desenvolve.

## Princípios

1. **Segurança desde o início (shift left).** Requisitos, modelagem de ameaças e revisão de código custam menos do que corrigir em produção.
2. **Automação com propósito.** Ferramentas ajudam a escalar, mas precisam de regras claras, triagem e contexto. Alerta ignorado não é controle.
3. **Responsabilidade compartilhada.** Segurança não é só do time de segurança. Quem escreve, revisa e opera também responde por ela.
4. **Privilégio mínimo em todo lugar.** Inclui contas de serviço, tokens de CI, permissões de pipeline e acesso a segredos.
5. **Evidência e rastreabilidade.** O pipeline deve registrar o que rodou, com qual versão e qual resultado.
6. **Falhe o build quando o risco justificar.** Um achado crítico não pode ser apenas um comentário no log.
7. **Não esconda achados.** Exceções precisam ser explícitas, justificadas, restritas e revisadas.

## Controles por fase

| Fase | Controle | Exemplo |
|------|----------|---------|
| Requisitos e design | Modelagem de ameaças, requisitos de segurança | STRIDE em um fluxo de login |
| Desenvolvimento | Padrões seguros, revisão de código, pre-commit | Consulta parametrizada, lint de segurança |
| Build e integração | SAST, SCA, testes de regressão, validação de configuração | Bandit, pip-audit, unittest |
| Artefato | Assinatura, SBOM, verificação de proveniência | Sigstore, CycloneDX |
| Deploy | IaC scanning, política de admissão, segredos gerenciados | Checkov, OPA, Vault |
| Operação | DAST autorizado, monitoramento, alerta, resposta | OWASP ZAP em staging, SIEM |
| Melhoria contínua | Métricas, retrospectivas, atualização de regras | Tempo médio de correção, taxa de falsos positivos |

## Tipos de ferramenta

- **SAST (Static Application Security Testing):** analisa código sem executá-lo. Exemplo em Python: Bandit, Semgrep. Bom para padrões conhecidos; não prova ausência de falhas.
- **SCA (Software Composition Analysis):** verifica dependências e licenças. Exemplo: pip-audit, Dependabot. Precisa considerar versão e caminho de exploração.
- **DAST (Dynamic Application Security Testing):** testa a aplicação em execução. Exemplo: OWASP ZAP. Só deve ser usado em ambiente autorizado.
- **IAST:** instrumenta a aplicação durante testes. Mais preciso, mais complexo de operar.
- **Secret scanning:** detecta credenciais commitadas. Exemplo: gitleaks, GitHub secret scanning.
- **IaC scanning:** verifica configuração de infraestrutura como código. Exemplo: Checkov, tfsec.
- **Container scanning:** verifica imagens e pacotes. Exemplo: Trivy.

Nenhuma ferramenta substitui revisão humana e contexto. Falso positivo sem triagem e falso negativo sem revisão são riscos reais.

## Pipeline seguro

Um pipeline de referência pode ter estes estágios:

1. **Validação de estrutura e sintaxe.** O projeto precisa estar íntegro antes de qualquer análise.
2. **Testes automatizados.** Inclua testes de regressão de segurança, não apenas testes funcionais.
3. **SAST.** Rode com regras adequadas ao projeto e falhe em achados de severidade alta não aprovados.
4. **SCA.** Verifique dependências declaradas e falhe em vulnerabilidades relevantes sem justificativa.
5. **Validação de configuração do agente.** Verifique frontmatter, registro de skills e caminhos documentados.
6. **Publicação de evidências.** Guarde relatórios e resultados como artefatos do workflow.

## Segurança do próprio CI/CD

O pipeline é um alvo valioso. Cuidados essenciais:

- Use `permissions` restritas no workflow, começando por `contents: read`.
- Não exponha segredos em logs, argumentos de linha de comando ou artefatos.
- Prefira ações oficiais e versões mantidas; quando o projeto exigir, fixe por SHA imutável.
- Não execute código de pull request com segredos de produção.
- Proteja branches e exija revisão.
- Revise workflows de terceiros antes de adotar.
- Trate dependências do próprio pipeline como parte da cadeia de suprimentos.

## Exceções e código intencionalmente vulnerável

Projetos educacionais podem conter exemplos deliberadamente inseguros. A exceção correta é:

- documentar claramente que o arquivo é um fixture de ensino;
- isolar o arquivo do restante do código;
- manter uma análise separada que mostre os achados;
- impedir que o fixture seja implantado;
- garantir que os checks de produção continuem falhando para vulnerabilidades reais.

Ocultar o achado com um `# nosec` genérico ou uma exclusão ampla destrói o valor educativo e a confiança no pipeline.

## Métricas úteis

- Tempo entre a introdução e a correção de uma vulnerabilidade.
- Percentual de achados triados versus ignorados.
- Cobertura de dependências e de testes de regressão.
- Taxa de falha do pipeline por achados reais.
- Quantidade de exceções ativas e sua idade.

Métricas não devem incentivar a redução artificial de achados. O objetivo é reduzir risco, não melhorar o número.

## O que este projeto implementa

O workflow `.github/workflows/security-checks.yml` cobre:

- sintaxe Python e testes automatizados;
- validação da estrutura das skills e do registro no `AGENTS.md`;
- análise estática com Bandit, isolando o exemplo vulnerável;
- verificação de dependências de desenvolvimento quando existe manifesto;
- validação de YAML dos arquivos do projeto.

Ele é uma base educacional, não um programa de segurança completo. DAST, scanning de containers, assinatura de artefatos e gestão de segredos em produção não estão implementados neste repositório.

## Referências

- NIST SP 800-218, Secure Software Development Framework: https://csrc.nist.gov/Projects/ssdf
- OWASP DevSecOps Guideline: https://owasp.org/www-project-devsecops-guideline/
- OWASP Top 10: https://owasp.org/Top10/
- SLSA: https://slsa.dev/
- GitHub Actions security hardening: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- Bandit: https://bandit.readthedocs.io/
- pip-audit: https://pypi.org/project/pip-audit/
