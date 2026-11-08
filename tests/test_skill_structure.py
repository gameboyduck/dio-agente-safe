"""Validação da estrutura do projeto, das skills e da configuração do agente.

Estes testes são intencionais e baratos: eles verificam que os arquivos
existem, que o frontmatter das skills é válido e que o roteamento em
AGENTS.md aponta para os caminhos corretos.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - dependência opcional de desenvolvimento
    yaml = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]

NEW_SKILLS = (
    "vulnerability-analysis",
    "security-testing",
    "security-learning-path",
)

ORIGINAL_SKILLS = (
    "study-plan",
    "unblock-challenge",
    "explain-concept",
    "web-search",
    "portfolio-review",
    "ai-builder-path",
)

REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "agent/persona.md",
    "agent/knowledge/security-basics.md",
    "agent/knowledge/vulnerability-classification.md",
    "agent/knowledge/secure-coding.md",
    "agent/knowledge/devsecops-basics.md",
    "skills/vulnerability-analysis/SKILL.md",
    "skills/vulnerability-analysis/README.md",
    "skills/security-testing/SKILL.md",
    "skills/security-testing/README.md",
    "skills/security-learning-path/SKILL.md",
    "skills/security-learning-path/README.md",
    "examples/sql-injection/app.py",
    "examples/sql-injection/app_secure.py",
    "examples/sql-injection/README.md",
    "tests/test_sql_injection.py",
    "tests/test_skill_structure.py",
    "tests/test_agent_behavior.md",
    "reports/sample-vulnerability-report.md",
    "docs/security-assessment-workflow.md",
    "docs/threat-modeling.md",
    "docs/evidence-guide.md",
    "docs/ubuntu-server-security.md",
    ".github/workflows/security-checks.yml",
)

REPORT_HEADINGS = (
    "# Security Vulnerability Assessment",
    "## 1. Executive Summary",
    "## 2. Assessment Context",
    "## 3. Vulnerability Identification",
    "## 4. Risk Assessment",
    "## 5. Technical Evidence",
    "## 6. Recommended Remediation",
    "## 7. Validation",
    "## 8. Final Assessment",
    "## 9. Learning Notes",
)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if match is None:
        raise AssertionError(f"{path} não possui frontmatter YAML delimitado por ---")

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


class ProjectStructureTests(unittest.TestCase):
    def test_required_paths_exist(self) -> None:
        missing = [path for path in REQUIRED_PATHS if not (PROJECT_ROOT / path).is_file()]
        self.assertEqual(missing, [], f"Arquivos obrigatórios ausentes: {missing}")

    def test_original_skills_are_preserved(self) -> None:
        missing = [
            skill
            for skill in ORIGINAL_SKILLS
            if not (PROJECT_ROOT / "skills" / skill / "SKILL.md").is_file()
        ]
        self.assertEqual(missing, [], f"Skills originais ausentes: {missing}")

    def test_new_skills_have_valid_frontmatter(self) -> None:
        for skill in NEW_SKILLS:
            with self.subTest(skill=skill):
                path = PROJECT_ROOT / "skills" / skill / "SKILL.md"
                metadata = parse_frontmatter(path)
                self.assertEqual(metadata.get("name"), skill)
                description = metadata.get("description", "")
                self.assertGreaterEqual(
                    len(description),
                    40,
                    "A description deve explicar quando a skill deve ser usada.",
                )

    def test_new_skills_have_human_readable_readme(self) -> None:
        for skill in NEW_SKILLS:
            with self.subTest(skill=skill):
                readme = PROJECT_ROOT / "skills" / skill / "README.md"
                text = readme.read_text(encoding="utf-8")
                self.assertGreater(len(text), 400)
                self.assertIn("## O que a skill faz", text)

    def test_skills_are_registered_in_agents_md(self) -> None:
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for skill in NEW_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(f"skills/{skill}/SKILL.md", agents)

    def test_skills_are_listed_in_readme(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        for skill in NEW_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(f"skills/{skill}/SKILL.md", readme)

    def test_knowledge_files_cover_required_concepts(self) -> None:
        expectations = {
            "security-basics.md": (
                "Vulnerabilidade",
                "Ameaça",
                "Risco",
                "Confidencialidade",
                "Integridade",
                "Disponibilidade",
                "Superfície de ataque",
                "Privilégio mínimo",
            ),
            "vulnerability-classification.md": (
                "OWASP",
                "CWE",
                "CVE",
                "CVSS",
                "MITRE ATT&CK",
                "A05:2025",
                "CWE-89",
                "T1190",
            ),
            "secure-coding.md": (
                "SQL Injection",
                "parametrizada",
                "pbkdf2_hmac",
                "subprocess",
                "pickle",
                "path traversal",
            ),
            "devsecops-basics.md": (
                "SAST",
                "SCA",
                "DAST",
                "CI/CD",
                "privilégio mínimo",
            ),
        }
        for filename, terms in expectations.items():
            path = PROJECT_ROOT / "agent" / "knowledge" / filename
            text = path.read_text(encoding="utf-8").casefold()
            for term in terms:
                with self.subTest(file=filename, term=term):
                    self.assertIn(term.casefold(), text)

    def test_report_template_is_complete_in_skill_and_sample(self) -> None:
        for relative in (
            "skills/vulnerability-analysis/SKILL.md",
            "reports/sample-vulnerability-report.md",
        ):
            text = (PROJECT_ROOT / relative).read_text(encoding="utf-8")
            for heading in REPORT_HEADINGS:
                with self.subTest(file=relative, heading=heading):
                    self.assertIn(heading, text)

    def test_persona_preserves_original_and_adds_cybersecurity(self) -> None:
        persona = (PROJECT_ROOT / "agent" / "persona.md").read_text(encoding="utf-8")
        self.assertIn("## Identidade", persona)
        self.assertIn("## Valores", persona)
        self.assertIn("## Especialização em cybersecurity", persona)
        self.assertIn("AppSec", persona)

    def test_agents_md_keeps_original_identity_and_adds_knowledge(self) -> None:
        agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Você é o DIO Agent", agents)
        for filename in (
            "security-basics.md",
            "vulnerability-classification.md",
            "secure-coding.md",
            "devsecops-basics.md",
        ):
            with self.subTest(filename=filename):
                self.assertIn(f"agent/knowledge/{filename}", agents)

    def test_readme_credits_original_project(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("digitalinnovationone/dio-agent", readme)
        self.assertIn("DIO Agent", readme)

    def test_ubuntu_scenario_documents_authorization_and_status(self) -> None:
        text = (PROJECT_ROOT / "docs" / "ubuntu-server-security.md").read_text(
            encoding="utf-8"
        )
        folded = text.casefold()
        self.assertIn("autorização", folded)
        self.assertIn("não foi executado", folded)
        self.assertIn("Pendente", text)

    def test_readme_relative_links_resolve(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme)
        missing = []
        for link in links:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = link.split("#", 1)[0]
            if target and not (PROJECT_ROOT / target).exists():
                missing.append(link)
        self.assertEqual(missing, [], f"Links locais quebrados no README: {missing}")

    def test_workflow_declares_required_triggers_and_permissions(self) -> None:
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "security-checks.yml"
        text = workflow_path.read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)
        self.assertIn("push:", text)
        self.assertIn("main", text)
        self.assertIn("permissions:", text)
        self.assertIn("contents: read", text)

    @unittest.skipUnless(yaml is not None, "PyYAML não instalado")
    def test_workflow_yaml_is_syntactically_valid(self) -> None:
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "security-checks.yml"
        data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        self.assertIn("jobs", data)
        self.assertGreaterEqual(len(data["jobs"]), 3)
        self.assertIn("contents", data.get("permissions", {}))

    @unittest.skipUnless(yaml is not None, "PyYAML não instalado")
    def test_all_project_yaml_files_are_valid(self) -> None:
        yaml_files = sorted(PROJECT_ROOT.glob("**/*.yml")) + sorted(
            PROJECT_ROOT.glob("**/*.yaml")
        )
        yaml_files = [
            path for path in yaml_files if ".git" not in path.parts
        ]
        self.assertTrue(yaml_files, "Nenhum arquivo YAML encontrado para validar.")
        for path in yaml_files:
            with self.subTest(path=str(path.relative_to(PROJECT_ROOT))):
                yaml.safe_load(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
