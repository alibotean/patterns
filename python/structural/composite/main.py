"""
Composite Pattern

Intent: Compose objects into tree structures to represent part-whole hierarchies.
Lets clients treat individual objects and compositions uniformly.

Example: a restaurant menu where MenuItems (leaves) and Menus (composites)
both respond to the same interface — the client never needs to distinguish them.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Component ─────────────────────────────────────────────────────────────────

class MenuComponent(ABC):
    """Common interface for both leaves (MenuItem) and composites (Menu)."""

    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def get_price(self) -> float: ...

    @abstractmethod
    def print(self, indent: str = "") -> None: ...


# ── Leaf ──────────────────────────────────────────────────────────────────────

class MenuItem(MenuComponent):
    """A leaf node — a single dish with a fixed price."""

    def __init__(self, name: str, price: float, description: str = "") -> None:
        self._name        = name
        self._price       = price
        self._description = description

    def get_name(self)  -> str:   return self._name
    def get_price(self) -> float: return self._price

    def print(self, indent: str = "") -> None:
        desc = f" — {self._description}" if self._description else ""
        print(f"{indent}🍽  {self._name:<22} ${self._price:.2f}{desc}")


# ── Composite ─────────────────────────────────────────────────────────────────

class Menu(MenuComponent):
    """
    A composite node — a named section that contains other components
    (MenuItems or nested Menus). get_price() recurses into all children.
    """

    def __init__(self, name: str) -> None:
        self._name:     str                    = name
        self._children: list[MenuComponent]   = []

    def add(self, component: MenuComponent) -> "Menu":
        """Fluent add — allows chaining."""
        self._children.append(component)
        return self

    def get_name(self)  -> str:   return self._name

    def get_price(self) -> float:
        """Total price = sum of all child prices, recursively."""
        return sum(child.get_price() for child in self._children)

    def print(self, indent: str = "") -> None:
        print(f"{indent}📋 {self._name}  (total: ${self.get_price():.2f})")
        for child in self._children:
            child.print(indent + "  ")


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Leaves
    espresso   = MenuItem("Espresso",        2.50, "single shot")
    cappuccino = MenuItem("Cappuccino",       3.75, "with steamed milk")
    croissant  = MenuItem("Croissant",        2.00, "butter pastry")
    omelette   = MenuItem("Cheese Omelette",  7.50, "3-egg, cheddar")
    pancakes   = MenuItem("Pancakes",         6.50, "with maple syrup")
    burger     = MenuItem("Classic Burger",  11.00, "beef, lettuce, tomato")
    fries      = MenuItem("Fries",            3.00, "crispy, salted")

    # Composites
    drinks    = Menu("☕ Drinks").add(espresso).add(cappuccino)
    breakfast = Menu("🌅 Breakfast").add(croissant).add(omelette).add(pancakes)
    lunch     = Menu("☀️  Lunch").add(burger).add(fries)

    # Root composite — the full menu
    full_menu = Menu("🍴 Full Menu").add(drinks).add(breakfast).add(lunch)

    # The client just calls print() on the root — it handles the whole tree
    full_menu.print()
