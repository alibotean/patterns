"""
Decorator Pattern

Intent: Attach additional responsibilities to an object dynamically, without subclassing.

Python has two natural ways to express this pattern:
  1. The classic OOP decorator (wrapping objects that share an interface).
  2. Python's built-in @ decorator syntax (wrapping callables).

Both are shown here. The OOP version matches the GoF pattern exactly;
the function version is the idiomatic Python application of the same idea.
"""

from __future__ import annotations
import time
import functools
from abc import ABC, abstractmethod


# ══════════════════════════════════════════════════════════════════════════════
# Part 1 — OOP Decorator (GoF-style)
# ══════════════════════════════════════════════════════════════════════════════

class TextRenderer(ABC):
    """Component interface: renders a piece of text."""
    @abstractmethod
    def render(self, text: str) -> str: ...


class PlainText(TextRenderer):
    """Concrete component — the base, undecorated renderer."""
    def render(self, text: str) -> str:
        return text


class TextDecorator(TextRenderer):
    """Base decorator: wraps a TextRenderer and delegates to it."""
    def __init__(self, wrapped: TextRenderer) -> None:
        self._wrapped = wrapped

    def render(self, text: str) -> str:
        return self._wrapped.render(text)  # default: just pass through


class BoldDecorator(TextDecorator):
    def render(self, text: str) -> str:
        return f"<b>{self._wrapped.render(text)}</b>"


class ItalicDecorator(TextDecorator):
    def render(self, text: str) -> str:
        return f"<i>{self._wrapped.render(text)}</i>"


class UpperCaseDecorator(TextDecorator):
    def render(self, text: str) -> str:
        return self._wrapped.render(text).upper()


# ══════════════════════════════════════════════════════════════════════════════
# Part 2 — Function decorator (Pythonic application of the same pattern)
# ══════════════════════════════════════════════════════════════════════════════

def retry(max_attempts: int = 3, delay: float = 0.0):
    """
    Decorator factory: wraps a function to retry on exception.
    Adding this responsibility doesn't require changing the function at all —
    the decorator adds it from the outside, just like the OOP version.
    """
    def decorator(func):
        @functools.wraps(func)   # preserves __name__, __doc__, etc.
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    print(f"  [retry] attempt {attempt} failed: {exc}")
                    if attempt == max_attempts:
                        raise
                    if delay:
                        time.sleep(delay)
        return wrapper
    return decorator


def logged(func):
    """Decorator: logs entry and exit of any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [log] → calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"  [log] ← {func.__name__} returned {result!r}")
        return result
    return wrapper


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== OOP Decorator ===")
    # Decorators stack like Russian dolls — order matters
    renderer = UpperCaseDecorator(BoldDecorator(ItalicDecorator(PlainText())))
    print(renderer.render("hello world"))   # <b><i>HELLO WORLD</i></b> ... wait
    # Note: UpperCase wraps Bold, which wraps Italic — so Italic is innermost
    # render order: PlainText → Italic → Bold → UpperCase
    print(ItalicDecorator(PlainText()).render("hello"))         # <i>hello</i>
    print(BoldDecorator(ItalicDecorator(PlainText())).render("hello"))  # <b><i>hello</i></b>

    print("\n=== Function Decorator ===")
    attempt_counter = {"n": 0}

    @retry(max_attempts=3)
    @logged
    def unreliable_api_call(x: int) -> str:
        attempt_counter["n"] += 1
        if attempt_counter["n"] < 3:          # fail the first two times
            raise ConnectionError("timeout")
        return f"result({x})"

    result = unreliable_api_call(42)
    print(f"Final result: {result}")
