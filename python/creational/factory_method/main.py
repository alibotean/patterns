"""
Factory Method Pattern

Intent: Define an interface for creating an object, but let subclasses decide
which class to instantiate.

Python approach: the "factory method" is a regular method that subclasses override.
No abstract base class is strictly required, but abc makes the contract explicit.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Product ───────────────────────────────────────────────────────────────────

class Exporter(ABC):
    """Every exporter can serialise a list of records to a string."""

    @abstractmethod
    def export(self, records: list[dict]) -> str: ...


# ── Concrete Products ─────────────────────────────────────────────────────────

class CsvExporter(Exporter):
    def export(self, records: list[dict]) -> str:
        if not records:
            return ""
        header = ",".join(records[0].keys())
        rows   = [",".join(str(v) for v in r.values()) for r in records]
        return "\n".join([header] + rows)


class JsonExporter(Exporter):
    import json as _json  # kept local to avoid polluting module namespace

    def export(self, records: list[dict]) -> str:
        import json
        return json.dumps(records, indent=2)


class MarkdownExporter(Exporter):
    def export(self, records: list[dict]) -> str:
        if not records:
            return ""
        keys   = list(records[0].keys())
        header = "| " + " | ".join(keys) + " |"
        sep    = "| " + " | ".join("---" for _ in keys) + " |"
        rows   = ["| " + " | ".join(str(r[k]) for k in keys) + " |" for r in records]
        return "\n".join([header, sep] + rows)


# ── Creator (abstract) ────────────────────────────────────────────────────────

class ReportService(ABC):
    """
    Declares the factory method that subclasses must implement.
    The business logic in `generate` uses the product via the abstract Exporter interface.
    """

    @abstractmethod
    def create_exporter(self) -> Exporter:
        """Factory method — subclasses decide what product to create."""
        ...

    def generate(self, title: str, records: list[dict]) -> None:
        """Template that uses the product without knowing its concrete type."""
        exporter = self.create_exporter()
        output   = exporter.export(records)
        print(f"=== {title} ({type(exporter).__name__}) ===")
        print(output)
        print()


# ── Concrete Creators ─────────────────────────────────────────────────────────

class CsvReportService(ReportService):
    def create_exporter(self) -> Exporter:
        return CsvExporter()


class JsonReportService(ReportService):
    def create_exporter(self) -> Exporter:
        return JsonExporter()


class MarkdownReportService(ReportService):
    def create_exporter(self) -> Exporter:
        return MarkdownExporter()


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = [
        {"name": "Alice", "dept": "Engineering", "salary": 95000},
        {"name": "Bob",   "dept": "Design",      "salary": 82000},
    ]

    services: list[ReportService] = [
        CsvReportService(),
        JsonReportService(),
        MarkdownReportService(),
    ]

    for service in services:
        service.generate("Employee Report", data)
