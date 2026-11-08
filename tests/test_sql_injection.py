"""Testes de regressão do laboratório de SQL Injection.

Os testes usam apenas bancos SQLite temporários e dados sintéticos. Nenhum
sistema externo é acessado.
"""

from __future__ import annotations

import ast
import importlib.util
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAB_DIR = PROJECT_ROOT / "examples" / "sql-injection"


def load_lab_module(module_name: str, filename: str):
    """Carrega app.py/app_secure.py sem transformar a pasta em pacote."""
    spec = importlib.util.spec_from_file_location(module_name, LAB_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Não foi possível carregar {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute_calls(filename: str) -> list[ast.Call]:
    tree = ast.parse((LAB_DIR / filename).read_text(encoding="utf-8"))
    calls = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "execute"
            and node.args
        ):
            calls.append(node)
    return calls


def imported_modules(filename: str) -> set[str]:
    tree = ast.parse((LAB_DIR / filename).read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


vulnerable = load_lab_module("dio_lab_sqli_vulnerable", "app.py")
secure = load_lab_module("dio_lab_sqli_secure", "app_secure.py")


class SqlInjectionLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._temporary = tempfile.TemporaryDirectory(prefix="dio-sqli-tests-")
        base = Path(cls._temporary.name)
        cls.vulnerable_db = base / "vulnerable.db"
        cls.secure_db = base / "secure.db"
        vulnerable.create_database(cls.vulnerable_db)
        secure.create_database(cls.secure_db)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._temporary.cleanup()

    def test_vulnerable_source_builds_sql_with_interpolation(self) -> None:
        """A versão vulnerável deve atribuir uma f-string com SQL a uma variável."""
        tree = ast.parse((LAB_DIR / "app.py").read_text(encoding="utf-8"))
        sql_fstrings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.JoinedStr):
                constants = [
                    value.value
                    for value in node.value.values
                    if isinstance(value, ast.Constant) and isinstance(value.value, str)
                ]
                if any("SELECT id FROM users" in text for text in constants):
                    sql_fstrings.append(node)

        self.assertTrue(
            sql_fstrings,
            "Era esperada uma consulta SQL construída com f-string em app.py.",
        )
        self.assertTrue(
            any(isinstance(call.args[0], ast.Name) for call in execute_calls("app.py")),
            "A consulta interpolada deve ser passada para execute().",
        )

    def test_secure_source_uses_parameterized_query(self) -> None:
        """A versão segura deve usar marcador ? e argumento separado."""
        calls = execute_calls("app_secure.py")
        parameterized = []
        for call in calls:
            first = call.args[0]
            if (
                isinstance(first, ast.Constant)
                and isinstance(first.value, str)
                and "WHERE username = ?" in first.value
                and len(call.args) >= 2
                and isinstance(call.args[1], ast.Tuple)
            ):
                parameterized.append(call)

        self.assertTrue(
            parameterized,
            "A consulta de autenticação segura deve usar '?' e uma tupla de parâmetros.",
        )

    def test_secure_source_uses_constant_time_comparison(self) -> None:
        source = (LAB_DIR / "app_secure.py").read_text(encoding="utf-8")
        self.assertIn("hmac.compare_digest", source)
        self.assertIn("pbkdf2_hmac", source)

    def test_normal_authentication_works_in_both_versions(self) -> None:
        self.assertTrue(vulnerable.authenticate(self.vulnerable_db, "alice", "senha-demo-123"))
        self.assertTrue(vulnerable.authenticate(self.vulnerable_db, "bob", "outra-senha-456"))
        self.assertTrue(secure.authenticate(self.secure_db, "alice", "senha-demo-123"))
        self.assertTrue(secure.authenticate(self.secure_db, "bob", "outra-senha-456"))

    def test_wrong_password_is_rejected_in_both_versions(self) -> None:
        self.assertFalse(vulnerable.authenticate(self.vulnerable_db, "alice", "senha-errada"))
        self.assertFalse(secure.authenticate(self.secure_db, "alice", "senha-errada"))

    def test_vulnerable_version_demonstrates_controlled_bypass(self) -> None:
        """Demonstração confinada ao banco temporário local do laboratório."""
        payload = "' OR '1'='1' --"
        self.assertTrue(
            vulnerable.authenticate(self.vulnerable_db, payload, "qualquer-coisa"),
            "A versão vulnerável deve demonstrar o bypass para fins didáticos.",
        )

    def test_secure_version_rejects_malicious_input_as_data(self) -> None:
        payloads = [
            "' OR '1'='1' --",
            "' OR 1=1 --",
            "alice' --",
            "' OR 'a'='a' --",
            "') OR ('1'='1",
            "admin'/*",
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                self.assertFalse(
                    secure.authenticate(self.secure_db, payload, "qualquer-coisa"),
                    f"Entrada maliciosa foi aceita: {payload!r}",
                )

    def test_secure_version_stores_hash_not_plaintext(self) -> None:
        with closing(sqlite3.connect(str(self.secure_db))) as connection:
            rows = connection.execute(
                "SELECT username, password_hash, salt FROM users"
            ).fetchall()

        self.assertEqual(len(rows), 2)
        for _username, password_hash, salt in rows:
            self.assertIsInstance(password_hash, bytes)
            self.assertEqual(len(password_hash), 32)
            self.assertIsInstance(salt, bytes)
            self.assertEqual(len(salt), 16)

        database_bytes = self.secure_db.read_bytes()
        for _username, password in secure.DEMO_USERS:
            self.assertNotIn(
                password.encode("utf-8"),
                database_bytes,
                "A senha em texto puro não deve aparecer no arquivo do banco.",
            )

    def test_secure_version_uses_unique_salts(self) -> None:
        with closing(sqlite3.connect(str(self.secure_db))) as connection:
            salts = [row[0] for row in connection.execute("SELECT salt FROM users")]
        self.assertEqual(len(salts), len(set(salts)))

    def test_lab_does_not_import_network_libraries(self) -> None:
        forbidden = {"requests", "httpx", "aiohttp", "socket", "http", "urllib"}
        for filename in ("app.py", "app_secure.py"):
            with self.subTest(filename=filename):
                self.assertFalse(
                    imported_modules(filename) & forbidden,
                    f"{filename} não deve importar bibliotecas de rede.",
                )
                source = (LAB_DIR / filename).read_text(encoding="utf-8")
                self.assertNotIn("http://", source)
                self.assertNotIn("https://", source)

    def test_databases_are_created_in_temporary_directory(self) -> None:
        self.assertEqual(self.vulnerable_db.parent, self.secure_db.parent)
        self.assertTrue(self.vulnerable_db.exists())
        self.assertTrue(self.secure_db.exists())


if __name__ == "__main__":
    unittest.main()
