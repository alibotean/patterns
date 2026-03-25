"""
Strategy Pattern

Intent: Define a family of algorithms, encapsulate each one, and make them
interchangeable so the algorithm can vary independently from the clients that use it.

Python approach: strategies can be plain callables (functions/lambdas) or classes.
Both are shown. Using callables is idiomatic Python and requires no interface boilerplate.

Example: a payment processor that supports multiple payment methods.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable


# ── Strategy as a class hierarchy (classic GoF) ───────────────────────────────

@dataclass
class PaymentDetails:
    amount:   float
    currency: str = "USD"


class PaymentStrategy(ABC):
    """Abstract strategy interface."""

    @abstractmethod
    def pay(self, details: PaymentDetails) -> bool:
        """Execute the payment. Returns True on success."""
        ...


class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str) -> None:
        # Store only a masked version — never log full card numbers
        self._masked = f"****-****-****-{card_number[-4:]}"
        self._cvv    = cvv

    def pay(self, details: PaymentDetails) -> bool:
        print(f"  [CreditCard] Charging {details.amount} {details.currency} "
              f"to card {self._masked}")
        return True


class PayPalStrategy(PaymentStrategy):
    def __init__(self, email: str) -> None:
        self._email = email

    def pay(self, details: PaymentDetails) -> bool:
        print(f"  [PayPal] Sending {details.amount} {details.currency} "
              f"via PayPal account {self._email}")
        return True


class CryptoStrategy(PaymentStrategy):
    def __init__(self, wallet_address: str, coin: str = "BTC") -> None:
        self._wallet = wallet_address
        self._coin   = coin

    def pay(self, details: PaymentDetails) -> bool:
        print(f"  [Crypto] Transferring {details.amount} {details.currency} "
              f"worth of {self._coin} to {self._wallet[:8]}…")
        return True


# ── Context ────────────────────────────────────────────────────────────────────

class Checkout:
    """
    Executes a payment using whichever strategy was injected.
    Changing the strategy at runtime requires no changes to this class.
    """

    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        """Swap the payment method at runtime (e.g., user changed their mind)."""
        self._strategy = strategy

    def complete_purchase(self, amount: float, currency: str = "USD") -> None:
        details = PaymentDetails(amount, currency)
        success = self._strategy.pay(details)
        status  = "succeeded" if success else "failed"
        print(f"  → Purchase {status}: {amount} {currency}")


# ── Strategy as plain callables (Pythonic alternative) ────────────────────────

# When the strategy has no state, a plain function is all you need.
SortKey = Callable[[dict], object]

def sort_by_name(records: list[dict], key: SortKey) -> list[dict]:
    """The algorithm (sorting) is fixed; the ordering key is the strategy."""
    return sorted(records, key=key)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Class-based strategies (payment) ===")
    checkout = Checkout(CreditCardStrategy("4111111111111234", "123"))
    checkout.complete_purchase(99.99)

    checkout.set_strategy(PayPalStrategy("alice@example.com"))
    checkout.complete_purchase(49.50)

    checkout.set_strategy(CryptoStrategy("1A2B3C4D5E6F7890abcd"))
    checkout.complete_purchase(200.00)

    print("\n=== Callable strategies (sorting) ===")
    products = [
        {"name": "Keyboard", "price": 79.99, "stock": 15},
        {"name": "Mouse",    "price": 29.99, "stock": 42},
        {"name": "Monitor",  "price": 349.00, "stock": 5},
    ]

    by_price = lambda p: p["price"]
    by_stock = lambda p: p["stock"]
    by_name  = lambda p: p["name"]

    for strategy, label in [(by_price, "price"), (by_stock, "stock"), (by_name, "name")]:
        sorted_products = sort_by_name(products, strategy)
        print(f"  Sorted by {label}: {[p['name'] for p in sorted_products]}")
