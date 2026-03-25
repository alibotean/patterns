"""
Builder Pattern

Intent: Separate the construction of a complex object from its representation so
the same construction process can create different representations.

Python approach: a fluent builder with method chaining.
Using __slots__ on the product enforces immutability after build().
"""

from __future__ import annotations
from dataclasses import dataclass, field


# ── Product ───────────────────────────────────────────────────────────────────

@dataclass(frozen=True)   # frozen = immutable once created
class Pizza:
    """
    A pizza is the product. All fields are set once by PizzaBuilder.
    frozen=True makes every field read-only after __init__.
    """
    size:        str                     # required: "small" | "medium" | "large"
    crust:       str                     # required: "thin" | "thick" | "stuffed"
    sauce:       str          = "tomato"
    cheese:      str          = "mozzarella"
    toppings:    tuple[str, ...]  = ()
    extra_cheese: bool        = False
    well_done:   bool         = False

    def __str__(self) -> str:
        toppings_str = ", ".join(self.toppings) or "none"
        return (
            f"{self.size.title()} pizza | crust: {self.crust} | sauce: {self.sauce} | "
            f"cheese: {self.cheese} | toppings: {toppings_str} | "
            f"extra cheese: {self.extra_cheese} | well done: {self.well_done}"
        )


# ── Builder ───────────────────────────────────────────────────────────────────

class PizzaBuilder:
    """
    Fluent builder for Pizza.
    Required fields go in __init__; optional ones have dedicated methods.
    Each setter returns self so calls can be chained.
    """

    def __init__(self, size: str, crust: str) -> None:
        # Required — no sensible defaults exist for these
        self._size   = size
        self._crust  = crust
        # Optional — set to defaults
        self._sauce        = "tomato"
        self._cheese       = "mozzarella"
        self._toppings:    list[str] = []
        self._extra_cheese = False
        self._well_done    = False

    def sauce(self, sauce: str)         -> "PizzaBuilder": self._sauce  = sauce;  return self
    def cheese(self, cheese: str)       -> "PizzaBuilder": self._cheese = cheese; return self
    def extra_cheese(self)              -> "PizzaBuilder": self._extra_cheese = True; return self
    def well_done(self)                 -> "PizzaBuilder": self._well_done    = True; return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        self._toppings.append(topping)
        return self

    def build(self) -> Pizza:
        """Validate inputs and construct the immutable Pizza product."""
        valid_sizes  = {"small", "medium", "large"}
        valid_crusts = {"thin", "thick", "stuffed"}
        if self._size  not in valid_sizes:  raise ValueError(f"Invalid size: {self._size}")
        if self._crust not in valid_crusts: raise ValueError(f"Invalid crust: {self._crust}")
        return Pizza(
            size         = self._size,
            crust        = self._crust,
            sauce        = self._sauce,
            cheese       = self._cheese,
            toppings     = tuple(self._toppings),
            extra_cheese = self._extra_cheese,
            well_done    = self._well_done,
        )


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Minimal — only required fields, everything else uses defaults
    plain = PizzaBuilder("medium", "thin").build()
    print("Plain  :", plain)

    # Fully customised via fluent chain
    loaded = (
        PizzaBuilder("large", "stuffed")
        .sauce("bbq")
        .cheese("cheddar")
        .add_topping("pepperoni")
        .add_topping("mushrooms")
        .add_topping("jalapeños")
        .extra_cheese()
        .well_done()
        .build()
    )
    print("Loaded :", loaded)
