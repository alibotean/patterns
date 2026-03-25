"""
Proxy Pattern

Intent: Provide a surrogate or placeholder for another object to control access to it.

Three common proxy flavours shown here:
  1. Virtual proxy  — lazy initialisation (create the real object on first use)
  2. Protection proxy — access control (check permissions before delegating)
  3. Logging proxy  — transparent logging of every call

Python approach: all three implement the same interface as the real subject,
so callers cannot tell a proxy from the real object.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import time


# ── Subject interface ─────────────────────────────────────────────────────────

class Database(ABC):
    @abstractmethod
    def query(self, sql: str) -> list[dict]: ...

    @abstractmethod
    def execute(self, sql: str) -> int: ...


# ── Real Subject ──────────────────────────────────────────────────────────────

class RealDatabase(Database):
    """
    Connecting to a database is expensive.  We don't want to do it
    unless at least one query is actually issued.
    """

    def __init__(self, connection_string: str) -> None:
        print(f"[RealDatabase] Connecting to {connection_string} …")
        time.sleep(0)  # simulate connection latency without blocking tests
        self._connected = True

    def query(self, sql: str) -> list[dict]:
        print(f"[RealDatabase] Executing query: {sql}")
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def execute(self, sql: str) -> int:
        print(f"[RealDatabase] Executing statement: {sql}")
        return 1  # rows affected


# ── 1. Virtual Proxy — lazy init ──────────────────────────────────────────────

class LazyDatabaseProxy(Database):
    """Creates the real connection only on the first actual call."""

    def __init__(self, connection_string: str) -> None:
        self._conn_str = connection_string
        self._real: RealDatabase | None = None  # no connection yet

    def _get_real(self) -> RealDatabase:
        if self._real is None:
            self._real = RealDatabase(self._conn_str)
        return self._real

    def query(self, sql: str)   -> list[dict]: return self._get_real().query(sql)
    def execute(self, sql: str) -> int:        return self._get_real().execute(sql)


# ── 2. Protection Proxy — access control ─────────────────────────────────────

class ProtectedDatabaseProxy(Database):
    """Allows reads to everyone; restricts writes to admin users."""

    def __init__(self, real: Database, role: str) -> None:
        self._real = real
        self._role = role

    def query(self, sql: str) -> list[dict]:
        return self._real.query(sql)   # reads are always allowed

    def execute(self, sql: str) -> int:
        if self._role != "admin":
            raise PermissionError(f"Role '{self._role}' is not allowed to execute statements")
        return self._real.execute(sql)


# ── 3. Logging Proxy — transparent logging ────────────────────────────────────

class LoggingDatabaseProxy(Database):
    """Logs every call with timing information."""

    def __init__(self, real: Database) -> None:
        self._real = real

    def _timed(self, method_name: str, sql: str, fn):
        start  = time.perf_counter()
        result = fn(sql)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[LogProxy] {method_name}({sql!r}) took {elapsed:.2f} ms")
        return result

    def query(self, sql: str)   -> list[dict]: return self._timed("query",   sql, self._real.query)
    def execute(self, sql: str) -> int:        return self._timed("execute", sql, self._real.execute)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Virtual Proxy (lazy init) ===")
    db = LazyDatabaseProxy("postgresql://localhost/mydb")
    print("Proxy created — no connection yet.")
    rows = db.query("SELECT * FROM users")   # connection made here
    print(rows)

    print("\n=== Protection Proxy ===")
    real_db   = RealDatabase("postgresql://localhost/mydb")
    guest_db  = ProtectedDatabaseProxy(real_db, role="guest")
    admin_db  = ProtectedDatabaseProxy(real_db, role="admin")

    guest_db.query("SELECT name FROM products")   # ok
    try:
        guest_db.execute("DELETE FROM orders")    # blocked
    except PermissionError as e:
        print(f"  PermissionError: {e}")
    admin_db.execute("DELETE FROM orders WHERE id=99")  # ok

    print("\n=== Logging Proxy ===")
    logging_db = LoggingDatabaseProxy(real_db)
    logging_db.query("SELECT COUNT(*) FROM users")
    logging_db.execute("UPDATE config SET value='x'")
