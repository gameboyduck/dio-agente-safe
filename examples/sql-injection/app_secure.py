"""Laboratório didático: versão segura da tela de login.

Esta versão corrige a causa raiz do SQL Injection:

1. a consulta usa um marcador de parâmetro (?) em vez de interpolar entrada;
2. a senha não é armazenada em texto puro: usamos PBKDF2-HMAC-SHA256 com salt.

Para produção, prefira Argon2id (argon2-cffi) ou scrypt e calibre os parâmetros.
O exemplo usa apenas a biblioteca padrão para manter o laboratório simples.

Execute a demonstração local com:

    python examples/sql-injection/app_secure.py
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

LAB_WARNING = (
    "[LABORATÓRIO] Versão segura para estudo local. "
    "Não é um sistema de autenticação pronto para produção."
)

DEMO_USERS = (
    ("alice", "senha-demo-123"),
    ("bob", "outra-senha-456"),
)

PBKDF2_ITERATIONS = 600_000
SALT_BYTES = 16


def hash_password(password: str, salt: bytes) -> bytes:
    """Deriva a senha com PBKDF2-HMAC-SHA256 e salt única."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )


def verify_password(password: str, salt: bytes, expected_hash: bytes) -> bool:
    """Compara hashes em tempo constante."""
    candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, expected_hash)


def create_database(db_path: str | Path) -> None:
    """Cria o banco temporário, com hash e salt em vez de senha em texto puro."""
    with closing(sqlite3.connect(str(db_path))) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, "
            "username TEXT NOT NULL UNIQUE, "
            "password_hash BLOB NOT NULL, "
            "salt BLOB NOT NULL)"
        )

        for username, password in DEMO_USERS:
            salt = secrets.token_bytes(SALT_BYTES)
            password_hash = hash_password(password, salt)
            connection.execute(
                "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt),
            )

        connection.commit()


def authenticate(db_path: str | Path, username: str, password: str) -> bool:
    """Autentica com consulta parametrizada e verificação de hash."""
    with closing(sqlite3.connect(str(db_path))) as connection:
        cursor = connection.execute(
            "SELECT id, password_hash, salt FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()

    if row is None:
        return False

    _user_id, expected_hash, salt = row
    return verify_password(password, salt, expected_hash)


def run_demo(db_path: str | Path) -> None:
    """Executa o mesmo roteiro controlado da versão vulnerável."""
    print(LAB_WARNING)
    print()
    print("1) Login com credenciais sintéticas válidas")
    print("   alice / senha-demo-123 ->", authenticate(db_path, "alice", "senha-demo-123"))
    print()
    print("2) Login com senha incorreta")
    print("   alice / senha-errada     ->", authenticate(db_path, "alice", "senha-errada"))
    print()
    print("3) A mesma entrada maliciosa controlada agora é apenas dado")
    payload = "' OR '1'='1' --"
    print(f"   usuário: {payload}")
    print("   resultado ->", authenticate(db_path, payload, "qualquer-coisa"))
    print()
    print("A consulta parametrizada impede que o payload altere a estrutura do SQL.")
    print("O hash com salt impede que a senha seja lida diretamente do banco.")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="dio-sqli-secure-lab-") as temporary_dir:
        db_path = Path(temporary_dir) / "lab.db"
        create_database(db_path)
        run_demo(db_path)


if __name__ == "__main__":
    main()
