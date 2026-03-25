package behavioral.memento;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Memento Pattern
 *
 * Intent: Without violating encapsulation, capture and externalize an object's
 * internal state so the object can be restored to this state later.
 *
 * Key roles:
 *   • Originator — creates mementos of its own state; restores from them
 *   • Memento    — an opaque snapshot (only the originator can read it)
 *   • Caretaker  — stores mementos but never inspects their contents
 *
 * Use when: You need undo/redo without exposing the originator's internals.
 */

// ── Memento ───────────────────────────────────────────────────────────────────

/**
 * Stores a snapshot of TextEditor's state.
 * Declared as an inner class of TextEditor so only TextEditor can access its fields —
 * this is what "without violating encapsulation" means in practice.
 */
class TextEditorMemento {
    // Package-private so only classes in this package see it,
    // but in a real design this would be a private inner class.
    final String text;
    final int    cursorPosition;

    TextEditorMemento(String text, int cursorPosition) {
        this.text           = text;
        this.cursorPosition = cursorPosition;
    }
}

// ── Originator ────────────────────────────────────────────────────────────────

/**
 * The text editor owns its state and knows how to save/restore it.
 * Clients (caretakers) never directly modify text or cursorPosition —
 * they use save()/restore() only.
 */
class TextEditor {
    private String text           = "";
    private int    cursorPosition = 0;

    public void type(String input) {
        // Insert at cursor position
        text = text.substring(0, cursorPosition) + input + text.substring(cursorPosition);
        cursorPosition += input.length();
        printState("typed  \"" + input + "\"");
    }

    public void moveCursor(int delta) {
        cursorPosition = Math.max(0, Math.min(text.length(), cursorPosition + delta));
        printState("moved cursor by " + delta);
    }

    /** Snapshot the current state — returns an opaque memento. */
    public TextEditorMemento save() {
        System.out.println("  [Saved snapshot]");
        return new TextEditorMemento(text, cursorPosition);
    }

    /** Restore state from a previously saved memento. */
    public void restore(TextEditorMemento memento) {
        text           = memento.text;
        cursorPosition = memento.cursorPosition;
        printState("restored snapshot");
    }

    private void printState(String action) {
        System.out.printf("  %-30s → text=\"%s\"  cursor=%d%n", action, text, cursorPosition);
    }
}

// ── Caretaker ────────────────────────────────────────────────────────────────

/**
 * Manages the undo history stack.
 * Stores mementos but treats them as opaque blobs — never reads their fields.
 */
class UndoManager {
    private final Deque<TextEditorMemento> history = new ArrayDeque<>();
    private final TextEditor               editor;

    UndoManager(TextEditor editor) { this.editor = editor; }

    /** Save the editor's current state before a mutating operation. */
    public void checkpoint() { history.push(editor.save()); }

    /** Restore the most recent checkpoint. */
    public void undo() {
        if (history.isEmpty()) { System.out.println("  Nothing to undo."); return; }
        editor.restore(history.pop());
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        TextEditor  editor  = new TextEditor();
        UndoManager undoMgr = new UndoManager(editor);

        undoMgr.checkpoint();   // snapshot 1: empty
        editor.type("Hello");

        undoMgr.checkpoint();   // snapshot 2: "Hello"
        editor.type(", World");

        undoMgr.checkpoint();   // snapshot 3: "Hello, World"
        editor.moveCursor(-5);

        System.out.println("\n--- undo ---");
        undoMgr.undo(); // back to snapshot 3: "Hello, World"

        System.out.println("\n--- undo ---");
        undoMgr.undo(); // back to snapshot 2: "Hello"

        System.out.println("\n--- undo ---");
        undoMgr.undo(); // back to snapshot 1: ""
    }
}
