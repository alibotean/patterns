"""
Visitor Pattern

Intent: Represent an operation to be performed on elements of an object structure.
Lets you define a new operation without changing the classes of the elements.

Python approach: singledispatch gives us true double-dispatch without the visitor
interface boilerplate. Both the classic OOP style and the singledispatch style are shown.

Example: a document object model (DOM) with Bold, Paragraph, and Image nodes.
Two visitors — an HTML renderer and a word counter — work on the same tree.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import singledispatch
from typing import Any


# ── Element types ──────────────────────────────────────────────────────────────

@dataclass
class Paragraph:
    text: str


@dataclass
class Bold:
    text: str


@dataclass
class Image:
    src:     str
    alt:     str = ""
    width:   int = 0
    height:  int = 0


@dataclass
class Document:
    title:    str
    elements: list[Any] = field(default_factory=list)

    def add(self, *elements) -> "Document":
        self.elements.extend(elements)
        return self


# ══════════════════════════════════════════════════════════════════════════════
# Part 1 — Classic OOP Visitor
# ══════════════════════════════════════════════════════════════════════════════

class DocumentVisitor(ABC):
    @abstractmethod
    def visit_paragraph(self, node: Paragraph) -> Any: ...
    @abstractmethod
    def visit_bold(self,      node: Bold)      -> Any: ...
    @abstractmethod
    def visit_image(self,     node: Image)     -> Any: ...
    @abstractmethod
    def visit_document(self,  node: Document)  -> Any: ...


class HtmlRenderer(DocumentVisitor):
    """Converts the document tree to an HTML string."""

    def visit_paragraph(self, node: Paragraph) -> str:
        return f"<p>{node.text}</p>"

    def visit_bold(self, node: Bold) -> str:
        return f"<strong>{node.text}</strong>"

    def visit_image(self, node: Image) -> str:
        return (f'<img src="{node.src}" alt="{node.alt}" '
                f'width="{node.width}" height="{node.height}">')

    def visit_document(self, node: Document) -> str:
        body  = "\n".join(self._dispatch(el) for el in node.elements)
        return f"<html><head><title>{node.title}</title></head><body>\n{body}\n</body></html>"

    def _dispatch(self, element) -> str:
        """Route each element to the right visit method."""
        if isinstance(element, Paragraph): return self.visit_paragraph(element)
        if isinstance(element, Bold):      return self.visit_bold(element)
        if isinstance(element, Image):     return self.visit_image(element)
        raise TypeError(f"Unknown element type: {type(element)}")


class WordCounter(DocumentVisitor):
    """Counts words in all text nodes; ignores images."""

    def visit_paragraph(self, node: Paragraph) -> int: return len(node.text.split())
    def visit_bold(self,      node: Bold)      -> int: return len(node.text.split())
    def visit_image(self,     node: Image)     -> int: return 0  # no text in images

    def visit_document(self, node: Document) -> int:
        return sum(self._dispatch(el) for el in node.elements)

    def _dispatch(self, element) -> int:
        if isinstance(element, Paragraph): return self.visit_paragraph(element)
        if isinstance(element, Bold):      return self.visit_bold(element)
        if isinstance(element, Image):     return self.visit_image(element)
        raise TypeError(f"Unknown element type: {type(element)}")


# ══════════════════════════════════════════════════════════════════════════════
# Part 2 — singledispatch Visitor (Pythonic, no interface boilerplate)
# ══════════════════════════════════════════════════════════════════════════════

@singledispatch
def to_markdown(node) -> str:
    """Fallback: unsupported node type."""
    raise TypeError(f"No markdown handler for {type(node)}")

@to_markdown.register
def _(node: Paragraph) -> str: return f"\n{node.text}\n"

@to_markdown.register
def _(node: Bold)      -> str: return f"**{node.text}**"

@to_markdown.register
def _(node: Image)     -> str: return f"![{node.alt}]({node.src})"

@to_markdown.register
def _(node: Document)  -> str:
    parts = [f"# {node.title}"] + [to_markdown(el) for el in node.elements]
    return "\n".join(parts)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    doc = Document("My Article").add(
        Paragraph("Welcome to the world of design patterns."),
        Bold("The Visitor pattern is particularly powerful."),
        Image("diagram.png", alt="UML diagram", width=600, height=400),
        Paragraph("It lets you add operations without changing element classes."),
    )

    print("=== HTML (classic visitor) ===")
    print(HtmlRenderer().visit_document(doc))

    print("\n=== Word count (classic visitor) ===")
    print(f"Total words: {WordCounter().visit_document(doc)}")

    print("\n=== Markdown (singledispatch visitor) ===")
    print(to_markdown(doc))
