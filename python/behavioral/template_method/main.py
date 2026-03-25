"""
Template Method Pattern

Intent: Define the skeleton of an algorithm in a base class, deferring specific steps
to subclasses. Subclasses redefine certain steps without changing the algorithm's structure.

Python approach: the template method is a regular method (often not final in Python
since there's no `final` keyword, but documented as such). Abstract steps use abc.

Example: a data pipeline that parses different formats but shares the same
read → validate → transform → load sequence.
"""

from __future__ import annotations
import csv
import io
import json
from abc import ABC, abstractmethod
from typing import Any


# ── Template (abstract base) ──────────────────────────────────────────────────

class DataPipeline(ABC):
    """
    Defines the ETL skeleton.
    Concrete subclasses override the parse() and transform() steps
    without ever touching read_source() or load() logic.
    """

    # ── Template method — the algorithm skeleton ──────────────────────────────
    def run(self, source: str) -> None:
        """
        Orchestrates the full ETL pipeline in the correct order.
        Do not override — override the individual steps instead.
        """
        print(f"\n[{self.__class__.__name__}] Starting pipeline for: {source!r}")
        raw     = self.read_source(source)
        records = self.parse(raw)           # abstract
        valid   = self.validate(records)    # concrete with a hook
        data    = self.transform(valid)     # abstract
        self.load(data)
        print(f"[{self.__class__.__name__}] Done — {len(data)} records loaded.")

    # ── Fixed steps (common to all pipelines) ─────────────────────────────────

    def read_source(self, source: str) -> str:
        """Simulates reading from a file or network source."""
        print(f"  [read]     Reading from {source!r}")
        # In a real implementation this would open a file or HTTP request
        return source  # here the source string IS the content for demo purposes

    def validate(self, records: list[dict]) -> list[dict]:
        """Default validation: drop records missing a required 'id' field."""
        valid = [r for r in records if r.get("id") is not None]
        dropped = len(records) - len(valid)
        if dropped:
            print(f"  [validate] Dropped {dropped} invalid record(s)")
        return valid

    def load(self, data: list[dict]) -> None:
        """Default loader: pretty-print to stdout (replace with DB insert, etc.)."""
        print(f"  [load]     Inserting {len(data)} record(s):")
        for record in data:
            print(f"             {record}")

    # ── Abstract steps (subclasses must implement) ────────────────────────────

    @abstractmethod
    def parse(self, raw: str) -> list[dict]:
        """Parse raw text into a list of record dicts."""
        ...

    @abstractmethod
    def transform(self, records: list[dict]) -> list[dict]:
        """Apply domain-specific transformations to validated records."""
        ...


# ── Concrete Pipelines ────────────────────────────────────────────────────────

class CsvPipeline(DataPipeline):
    """Handles CSV data."""

    def parse(self, raw: str) -> list[dict]:
        reader  = csv.DictReader(io.StringIO(raw))
        records = list(reader)
        print(f"  [parse]    Parsed {len(records)} CSV row(s)")
        return records

    def transform(self, records: list[dict]) -> list[dict]:
        # Normalise: strip whitespace, cast numeric fields
        result = []
        for r in records:
            result.append({
                "id":    int(r["id"]),
                "name":  r["name"].strip().title(),
                "score": float(r["score"]),
            })
        print(f"  [transform] Normalised {len(result)} CSV record(s)")
        return result


class JsonPipeline(DataPipeline):
    """Handles JSON data."""

    def parse(self, raw: str) -> list[dict]:
        records = json.loads(raw)
        print(f"  [parse]    Parsed {len(records)} JSON object(s)")
        return records

    def transform(self, records: list[dict]) -> list[dict]:
        # Normalise: ensure all names are uppercase, scores are clamped 0-100
        result = []
        for r in records:
            result.append({
                "id":    r["id"],
                "name":  r["name"].upper(),
                "score": max(0, min(100, r.get("score", 0))),
            })
        print(f"  [transform] Normalised {len(result)} JSON record(s)")
        return result


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    csv_data = "id,name,score\n1, alice ,92\n2, bob ,85\n,carol,78"   # missing id on carol
    json_data = '[{"id":10,"name":"dave","score":110},{"id":11,"name":"eve","score":77}]'

    CsvPipeline().run(csv_data)
    JsonPipeline().run(json_data)
