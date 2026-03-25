"""
State Pattern

Intent: Allow an object to alter its behaviour when its internal state changes.
The object appears to change its class.

Python approach: each state is a class; the context delegates all behaviour to
the current state object. States can be swapped at runtime.

Example: an e-commerce order lifecycle.
  Pending → Processing → Shipped → Delivered
  Each state only allows certain transitions — invalid ones raise an error.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── State interface ────────────────────────────────────────────────────────────

class OrderState(ABC):
    """
    Declares all the actions that can be taken on an order.
    Each concrete state implements only the transitions that are valid from it.
    """

    def pay(self, order: "Order") -> None:
        raise InvalidTransitionError(f"Cannot pay in state '{self.__class__.__name__}'")

    def process(self, order: "Order") -> None:
        raise InvalidTransitionError(f"Cannot process in state '{self.__class__.__name__}'")

    def ship(self, order: "Order") -> None:
        raise InvalidTransitionError(f"Cannot ship in state '{self.__class__.__name__}'")

    def deliver(self, order: "Order") -> None:
        raise InvalidTransitionError(f"Cannot deliver in state '{self.__class__.__name__}'")

    def cancel(self, order: "Order") -> None:
        raise InvalidTransitionError(f"Cannot cancel in state '{self.__class__.__name__}'")

    @property
    @abstractmethod
    def label(self) -> str: ...


class InvalidTransitionError(Exception):
    pass


# ── Context ────────────────────────────────────────────────────────────────────

class Order:
    """
    The context. Delegates all state-specific behaviour to the current state.
    Client code calls order.ship() — it never instantiates state objects directly.
    """

    def __init__(self, order_id: str) -> None:
        self._order_id = order_id
        self._state: OrderState = PendingState()
        print(f"[Order {order_id}] Created — state: {self._state.label}")

    def set_state(self, state: OrderState) -> None:
        """Called by concrete states during a transition."""
        self._state = state
        print(f"[Order {self._order_id}] → {state.label}")

    @property
    def status(self) -> str: return self._state.label

    def pay(self)     -> None: self._state.pay(self)
    def process(self) -> None: self._state.process(self)
    def ship(self)    -> None: self._state.ship(self)
    def deliver(self) -> None: self._state.deliver(self)
    def cancel(self)  -> None: self._state.cancel(self)


# ── Concrete States ────────────────────────────────────────────────────────────

class PendingState(OrderState):
    """Waiting for payment. Can be paid or cancelled."""
    label = "Pending"

    def pay(self, order: Order) -> None:
        order.set_state(ProcessingState())

    def cancel(self, order: Order) -> None:
        order.set_state(CancelledState())


class ProcessingState(OrderState):
    """Payment received; being prepared. Can be shipped or cancelled."""
    label = "Processing"

    def ship(self, order: Order) -> None:
        order.set_state(ShippedState())

    def cancel(self, order: Order) -> None:
        order.set_state(CancelledState())


class ShippedState(OrderState):
    """In transit. Can only move forward to Delivered — no cancellation."""
    label = "Shipped"

    def deliver(self, order: Order) -> None:
        order.set_state(DeliveredState())


class DeliveredState(OrderState):
    """Terminal success state — no further transitions allowed."""
    label = "Delivered"


class CancelledState(OrderState):
    """Terminal failure state — no further transitions allowed."""
    label = "Cancelled"


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Happy path ===")
    order = Order("ORD-001")
    order.pay()
    order.process()
    order.ship()
    order.deliver()
    print(f"Final status: {order.status}")

    print("\n=== Cancelled after processing ===")
    order2 = Order("ORD-002")
    order2.pay()
    order2.cancel()
    print(f"Final status: {order2.status}")

    print("\n=== Invalid transition ===")
    order3 = Order("ORD-003")
    try:
        order3.ship()    # Can't ship without paying first
    except InvalidTransitionError as e:
        print(f"  Error: {e}")
