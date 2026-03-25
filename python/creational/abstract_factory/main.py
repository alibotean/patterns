"""
Abstract Factory Pattern

Intent: Provide an interface for creating families of related objects without
specifying their concrete classes.

Each factory produces a consistent *family* of products. Swapping the factory
swaps the whole family — client code stays unchanged.

Example: a UI theme system where Dark and Light themes each provide a Button
and a Tooltip widget that look and behave consistently together.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Abstract Products ─────────────────────────────────────────────────────────

class Button(ABC):
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def on_click(self) -> None: ...


class Tooltip(ABC):
    @abstractmethod
    def show(self, text: str) -> None: ...


# ── Light theme family ────────────────────────────────────────────────────────

class LightButton(Button):
    def render(self)     -> None: print("  [Light] White button with dark border")
    def on_click(self)   -> None: print("  [Light] Button pressed — subtle ripple animation")


class LightTooltip(Tooltip):
    def show(self, text: str) -> None:
        print(f"  [Light] ╭─ {text} ─╮  (white background, grey text)")


# ── Dark theme family ─────────────────────────────────────────────────────────

class DarkButton(Button):
    def render(self)     -> None: print("  [Dark] Charcoal button with neon accent border")
    def on_click(self)   -> None: print("  [Dark] Button pressed — glowing pulse animation")


class DarkTooltip(Tooltip):
    def show(self, text: str) -> None:
        print(f"  [Dark] ╭─ {text} ─╮  (dark background, white text)")


# ── Abstract Factory ──────────────────────────────────────────────────────────

class ThemeFactory(ABC):
    """One factory per theme; each factory creates all widgets in that theme."""

    @abstractmethod
    def create_button(self)  -> Button: ...

    @abstractmethod
    def create_tooltip(self) -> Tooltip: ...


# ── Concrete Factories ────────────────────────────────────────────────────────

class LightThemeFactory(ThemeFactory):
    def create_button(self)  -> Button:  return LightButton()
    def create_tooltip(self) -> Tooltip: return LightTooltip()


class DarkThemeFactory(ThemeFactory):
    def create_button(self)  -> Button:  return DarkButton()
    def create_tooltip(self) -> Tooltip: return DarkTooltip()


# ── Client ────────────────────────────────────────────────────────────────────

class Application:
    """
    Only depends on the abstract factory and abstract product types.
    Swapping the factory at construction time changes the entire look.
    """

    def __init__(self, factory: ThemeFactory) -> None:
        # Products are created via the factory — Application never names concrete types
        self._button  = factory.create_button()
        self._tooltip = factory.create_tooltip()

    def render(self) -> None:
        self._button.render()
        self._tooltip.show("Click to submit")

    def interact(self) -> None:
        self._button.on_click()


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for factory, label in [(LightThemeFactory(), "Light"), (DarkThemeFactory(), "Dark")]:
        print(f"--- {label} theme ---")
        app = Application(factory)
        app.render()
        app.interact()
        print()
