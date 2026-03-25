"""
Flyweight Pattern

Intent: Use sharing to support large numbers of fine-grained objects efficiently.

Split object state into:
  • Intrinsic state — shared, immutable (stored in the flyweight)
  • Extrinsic state — unique per context, passed in at call time

Python approach: a factory backed by a dict cache is idiomatic.
Using __slots__ on the flyweight prevents accidental mutation of shared state.
"""

from __future__ import annotations
import random
import sys


# ── Flyweight (intrinsic state) ───────────────────────────────────────────────

class CharacterStyle:
    """
    Stores the intrinsic (shared) state of a character's visual style.
    One instance per (font, size, bold, italic) combination — never per character.

    __slots__ prevents adding new attributes, keeping the object small.
    """
    __slots__ = ("font", "size", "bold", "italic")

    def __init__(self, font: str, size: int, bold: bool, italic: bool) -> None:
        self.font   = font
        self.size   = size
        self.bold   = bold
        self.italic = italic

    def render(self, char: str, x: int, y: int) -> None:
        """
        Renders the character using intrinsic state (self) +
        extrinsic state (char, x, y) that is passed in — NOT stored here.
        """
        flags = ("B" if self.bold else "") + ("I" if self.italic else "")
        print(f"  '{char}' at ({x},{y})  font={self.font} size={self.size} {flags or 'plain'}")

    def __repr__(self) -> str:
        return f"CharacterStyle({self.font}, {self.size}, bold={self.bold}, italic={self.italic})"


# ── Flyweight Factory ─────────────────────────────────────────────────────────

class StyleFactory:
    """
    Returns existing CharacterStyle instances for repeated (font, size, bold, italic)
    combinations, creating new ones only when genuinely new styles are requested.
    """
    _cache: dict[tuple, CharacterStyle] = {}

    @classmethod
    def get_style(cls, font: str, size: int,
                  bold: bool = False, italic: bool = False) -> CharacterStyle:
        key = (font, size, bold, italic)
        if key not in cls._cache:
            print(f"  [StyleFactory] Creating new style: {key}")
            cls._cache[key] = CharacterStyle(font, size, bold, italic)
        return cls._cache[key]

    @classmethod
    def cache_size(cls) -> int:
        return len(cls._cache)


# ── Context (extrinsic state) ─────────────────────────────────────────────────

class DocumentCharacter:
    """
    Represents one character in a document.
    Stores only the unique, position-specific state (char, x, y) and a
    *reference* to the shared CharacterStyle flyweight — not a copy.
    """
    __slots__ = ("char", "x", "y", "style")

    def __init__(self, char: str, x: int, y: int, style: CharacterStyle) -> None:
        self.char  = char
        self.x     = x
        self.y     = y
        self.style = style   # shared flyweight reference

    def render(self) -> None:
        self.style.render(self.char, self.x, self.y)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Build a short "document" of 12 characters using only 3 distinct styles
    LOREM = "Hello, World"
    styles_spec = [
        ("Arial",   12, False, False),
        ("Arial",   12, True,  False),  # bold
        ("Courier", 10, False, True),   # italic
    ]

    print("=== Requesting styles ===")
    characters = []
    for i, ch in enumerate(LOREM):
        spec  = styles_spec[i % len(styles_spec)]
        style = StyleFactory.get_style(*spec)
        characters.append(DocumentCharacter(ch, x=i * 10, y=0, style=style))

    print("\n=== Rendering document ===")
    for dc in characters:
        dc.render()

    print(f"\nTotal characters : {len(characters)}")
    print(f"Unique styles    : {StyleFactory.cache_size()}")
    # 12 characters, but only 3 CharacterStyle objects in memory
