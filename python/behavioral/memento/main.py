"""
Memento Pattern

Intent: Without violating encapsulation, capture and externalise an object's internal
state so it can be restored later.

Python approach: the Memento is a simple frozen dataclass — the originator creates and
reads it; the caretaker only stores/retrieves it as an opaque value.

Example: a drawing canvas that supports multi-level undo/redo.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy


# ── Memento ────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CanvasMemento:
    """
    An immutable snapshot of the canvas state.
    frozen=True prevents the caretaker from modifying the saved state.
    The shapes list is deep-copied on creation so later mutations don't affect it.
    """
    shapes: tuple  # immutable snapshot of the shape list


# ── Originator ────────────────────────────────────────────────────────────────

@dataclass
class Shape:
    kind:  str
    x:     int
    y:     int
    color: str

    def __str__(self) -> str:
        return f"{self.kind}({self.x},{self.y},{self.color})"


class Canvas:
    """
    The originator. Creates mementos of its own state and can restore from them.
    No other class can meaningfully inspect a memento — the structure is only
    useful to Canvas itself.
    """

    def __init__(self) -> None:
        self._shapes: list[Shape] = []

    def add_shape(self, shape: Shape) -> None:
        self._shapes.append(shape)
        print(f"  Canvas: added {shape}")

    def remove_last(self) -> None:
        if self._shapes:
            removed = self._shapes.pop()
            print(f"  Canvas: removed {removed}")

    def save(self) -> CanvasMemento:
        """Snapshot current state — deep-copy so future mutations don't bleed in."""
        snapshot = CanvasMemento(shapes=tuple(deepcopy(self._shapes)))
        print(f"  Canvas: saved snapshot ({len(snapshot.shapes)} shapes)")
        return snapshot

    def restore(self, memento: CanvasMemento) -> None:
        """Restore from a previously saved snapshot."""
        self._shapes = list(deepcopy(memento.shapes))  # deep-copy to stay independent
        print(f"  Canvas: restored snapshot ({len(self._shapes)} shapes)")

    def show(self) -> None:
        shapes_str = ", ".join(str(s) for s in self._shapes) or "(empty)"
        print(f"  Canvas state: [{shapes_str}]")


# ── Caretaker ─────────────────────────────────────────────────────────────────

class History:
    """
    Manages undo/redo stacks.
    Stores mementos but never reads their internal fields — treats them as opaque.
    """

    def __init__(self, canvas: Canvas) -> None:
        self._canvas:    Canvas               = canvas
        self._undo_stack: list[CanvasMemento] = []
        self._redo_stack: list[CanvasMemento] = []

    def save(self) -> None:
        """Save current state before a mutating operation."""
        self._undo_stack.append(self._canvas.save())
        self._redo_stack.clear()  # a new action invalidates the redo history

    def undo(self) -> None:
        if not self._undo_stack:
            print("  Nothing to undo.")
            return
        # Push current state to redo before restoring
        self._redo_stack.append(self._canvas.save())
        self._canvas.restore(self._undo_stack.pop())

    def redo(self) -> None:
        if not self._redo_stack:
            print("  Nothing to redo.")
            return
        self._undo_stack.append(self._canvas.save())
        self._canvas.restore(self._redo_stack.pop())


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    canvas  = Canvas()
    history = History(canvas)

    history.save()
    canvas.add_shape(Shape("Circle",    10, 20, "red"))

    history.save()
    canvas.add_shape(Shape("Rectangle", 30, 40, "blue"))

    history.save()
    canvas.add_shape(Shape("Triangle",  50, 60, "green"))

    print("\nCurrent state:"); canvas.show()

    print("\n--- Undo (remove triangle) ---")
    history.undo(); canvas.show()

    print("\n--- Undo (remove rectangle) ---")
    history.undo(); canvas.show()

    print("\n--- Redo (restore rectangle) ---")
    history.redo(); canvas.show()

    print("\n--- Undo all the way ---")
    history.undo(); canvas.show()
    history.undo(); canvas.show()
    history.undo(); canvas.show()   # nothing left to undo
