"""Laboratório didático: SQL Injection em uma tela de login.

AVISO: este arquivo é intencionalmente inseguro.
Ele existe apenas para demonstrar por que a entrada do usuário nunca deve ser
concatenada em uma consulta SQL. Não use este código em produção, não o exponha
na rede e não o adapte para dados reais.

Execute a demonstração local com:

    python examples/sql-injection/app.py

O banco SQLite é criado em um diretório temporário e apagado ao final.
"""

from __future__ import annotations

import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

LAB_WARNING = (
    "[LABORATÓRIO] Código intencionalmente vulnerável. "
    "Uso exclusivo para estudo local. Nunca implante em produção."
)

# Contas sintéticas. As senhas ficam em texto puro de propósito, porque este
# arquivo também demonstra o que não fazer com credenciais.
DEMO_USERS = (
    ("alice", "senha-demo-123"),
    ("bob", "outra-senha-456"),
)


def create_database(db_path: str | Path) -> None:
    """Cria o banco temporário e insere contas sintéticas."""
    with closing(sqlite3.connect(str(db_path))) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY, "
            "username TEXT NOT NULL UNIQUE, "
            "password TEXT NOT NULL)"
        )
        connection.executemany(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            DEMO_USERS,
        )
        connection.commit()


def authenticate(db_path: str | Path, username: str, password: str) -> bool:
    """Autentica um usuário usando uma consulta montada por interpolação.

    A falha está aqui: a entrada do usuário vira parte da linguagem SQL.
    """
    with closing(sqlite3.connect(str(db_path))) as connection:
        query = (
            "SELECT id FROM users "
            f"WHERE username = '{username}' AND password = '{password}'"
        )
        cursor = connection.execute(query)
        return cursor.fetchone() is not None


def run_demo(db_path: str | Path) -> None:
    """Executa um roteiro controlado, sem entrada interativa."""
    print(LAB_WARNING)
    print()
    print("1) Login com credenciais sintéticas válidas")
    print("   alice / senha-demo-123 ->", authenticate(db_path, "alice", "senha-demo-123"))
    print()
    print("2) Login com senha incorreta")
    print("   alice / senha-errada     ->", authenticate(db_path, "alice", "senha-errada"))
    print()
    print("3) Entrada maliciosa controlada: o texto vira parte da consulta")
    payload = "' OR '1'='1' --"
    print(f"   usuário: {payload}")
    print("   resultado ->", authenticate(db_path, payload, "qualquer-coisa"))
    print()
    print("Observe: o passo 3 retorna True sem senha válida.")
    print("Agora compare com app_secure.py e veja o mesmo teste falhar.")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="dio-sqli-lab-") as temporary_dir:
        db_path = Path(temporary_dir) / "lab.db"
        create_database(db_path)
        run_demo(db_path)


if __name__ == "__main__":
    main()
