"""
Prototype Pattern

Intent: Create new objects by copying a prototypical instance rather than calling
constructors directly.

Python approach: the standard library's copy.deepcopy() does the heavy lifting.
A custom __copy__ / __deepcopy__ can be provided when the default behaviour needs
adjusting (e.g., shallow-copy some fields, deep-copy others).
"""

import copy
from dataclasses import dataclass, field


# ── Prototype base ────────────────────────────────────────────────────────────

class Prototype:
    """
    Mixin that adds clone() to any class.
    Uses deepcopy so nested mutable objects are fully independent.
    """

    def clone(self) -> "Prototype":
        """Return a fully independent deep copy of this object."""
        return copy.deepcopy(self)


# ── Concrete Prototypes ───────────────────────────────────────────────────────

@dataclass
class Weapon(Prototype):
    name:    str
    damage:  int
    effects: list[str] = field(default_factory=list)  # mutable — deep-copy matters


@dataclass
class Enemy(Prototype):
    """
    A game enemy that is expensive to fully initialise (AI graph, pathfinding
    data, asset refs). Clone a pre-built prototype and tweak just the diff.
    """
    name:       str
    hp:         int
    position:   list[int]          # [x, y] — mutable, must be independent
    weapon:     Weapon | None = None
    is_boss:    bool          = False

    def move_to(self, x: int, y: int) -> None:
        self.position = [x, y]

    def __str__(self) -> str:
        weapon_name = self.weapon.name if self.weapon else "none"
        return (
            f"{self.name:12s}  hp={self.hp:>4}  pos={self.position}  "
            f"weapon={weapon_name}  boss={self.is_boss}"
        )


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Define prototypes once (imagine expensive setup here) ──────────────
    sword      = Weapon("Iron Sword", damage=35, effects=["bleed"])
    orc_proto  = Enemy("Orc",  hp=80,  position=[0, 0], weapon=sword)
    boss_proto = Enemy("Orc Warlord", hp=500, position=[0, 0],
                       weapon=Weapon("War Axe", damage=90, effects=["stun", "bleed"]),
                       is_boss=True)

    print("Prototypes:")
    print(" ", orc_proto)
    print(" ", boss_proto)
    print()

    # ── Clone and place instances — only position differs ─────────────────
    orc1 = orc_proto.clone(); orc1.move_to(10, 20); orc1.name = "Orc #1"
    orc2 = orc_proto.clone(); orc2.move_to(30, 40); orc2.name = "Orc #2"

    # Mutating a clone's weapon effects does NOT affect the prototype
    orc1.weapon.effects.append("poison")

    print("Clones:")
    print(" ", orc1)
    print(" ", orc2)
    print(" ", boss_proto.clone())

    # Verify independence
    print()
    print("Prototype weapon effects unchanged?",
          orc_proto.weapon.effects)         # ['bleed'] — not poisoned
    print("orc1 and orc2 share position?",
          orc1.position is orc2.position)   # False — fully independent
