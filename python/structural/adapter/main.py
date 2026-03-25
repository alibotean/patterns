"""
Adapter Pattern

Intent: Convert the interface of a class into another interface that clients expect,
letting otherwise-incompatible classes work together.

Python approach: the adapter inherits from (or simply implements) the target interface
and wraps the adaptee. Python's duck-typing means a formal base class is optional,
but using one makes the contract visible.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Target interface — what the rest of the app expects ───────────────────────

class DataReader(ABC):
    """The application reads data as a list of dicts (row-oriented records)."""

    @abstractmethod
    def read(self, source: str) -> list[dict]: ...


# ── Adaptee — a legacy library with an incompatible interface ─────────────────

class LegacyCsvParser:
    """
    A third-party CSV parser we cannot modify.
    Returns rows as lists of strings, not dicts.
    """

    def parse_csv(self, filepath: str) -> list[list[str]]:
        print(f"[LegacyCsvParser] Parsing file: {filepath}")
        # Simulated data — first row is the header
        return [
            ["id", "name",  "score"],
            ["1",  "Alice", "92"],
            ["2",  "Bob",   "85"],
            ["3",  "Carol", "78"],
        ]


# ── Adapter ───────────────────────────────────────────────────────────────────

class CsvDataReaderAdapter(DataReader):
    """
    Wraps LegacyCsvParser and translates its output (list of lists) into
    the list-of-dicts format that DataReader consumers expect.
    """

    def __init__(self, parser: LegacyCsvParser) -> None:
        self._parser = parser

    def read(self, source: str) -> list[dict]:
        raw_rows = self._parser.parse_csv(source)

        if not raw_rows:
            return []

        # First row is the header; zip each subsequent row against it
        header, *data_rows = raw_rows
        return [dict(zip(header, row)) for row in data_rows]


# ── Client code — only knows about DataReader ─────────────────────────────────

def print_report(reader: DataReader, source: str) -> None:
    """Accepts any DataReader — has no idea whether it's CSV, JSON, or adapted."""
    records = reader.read(source)
    for record in records:
        print("  ", record)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    legacy_parser = LegacyCsvParser()
    adapter       = CsvDataReaderAdapter(legacy_parser)

    # The client calls the target interface — the adaptation is invisible
    print_report(adapter, "scores.csv")
