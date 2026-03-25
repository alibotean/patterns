package behavioral.command;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * Command Pattern
 *
 * Intent: Encapsulate a request as an object, letting you parameterize clients,
 * queue or log requests, and support undoable operations.
 *
 * Key roles:
 *   • Command   — encapsulates the action + receiver reference
 *   • Receiver  — the object that actually does the work
 *   • Invoker   — triggers commands, optionally maintaining history for undo
 *   • Client    — creates concrete commands and wires them to the invoker
 */

// ── Command interface ────────────────────────────────────────────────────────

interface Command {
    void execute();
    void undo();
}

// ── Receiver ─────────────────────────────────────────────────────────────────

/** The text editor is the receiver — it knows how to perform the actual operations. */
class TextEditor {
    private StringBuilder text = new StringBuilder();

    public void insertText(String s) {
        text.append(s);
        System.out.println("  Editor: \"" + text + "\"");
    }

    public void deleteText(int numChars) {
        int len = text.length();
        text.delete(Math.max(0, len - numChars), len);
        System.out.println("  Editor: \"" + text + "\"");
    }

    public String getText() { return text.toString(); }
}

// ── Concrete Commands ─────────────────────────────────────────────────────────

/** Inserts a string; undo removes those same characters. */
class InsertCommand implements Command {
    private final TextEditor editor;
    private final String     text;

    InsertCommand(TextEditor editor, String text) {
        this.editor = editor;
        this.text   = text;
    }

    @Override public void execute() { editor.insertText(text); }
    @Override public void undo()    { editor.deleteText(text.length()); }
}

/** Deletes the last N characters; undo re-inserts the saved content. */
class DeleteCommand implements Command {
    private final TextEditor editor;
    private final int        count;
    private String           deletedText = ""; // saved for undo

    DeleteCommand(TextEditor editor, int count) {
        this.editor = editor;
        this.count  = count;
    }

    @Override
    public void execute() {
        String current = editor.getText();
        int from = Math.max(0, current.length() - count);
        deletedText = current.substring(from); // save before deleting
        editor.deleteText(count);
    }

    @Override
    public void undo() {
        editor.insertText(deletedText); // restore exactly what was removed
    }
}

// ── Invoker ──────────────────────────────────────────────────────────────────

/**
 * The Invoker executes commands and keeps a history stack for undo.
 * It doesn't know what TextEditor is — it only knows about Command.
 */
class CommandHistory {
    private final Deque<Command> history = new ArrayDeque<>();

    /** Execute a command and push it onto the history stack. */
    public void execute(Command cmd) {
        cmd.execute();
        history.push(cmd);
    }

    /** Undo the most recent command by popping it from the stack. */
    public void undo() {
        if (history.isEmpty()) {
            System.out.println("  Nothing to undo.");
            return;
        }
        history.pop().undo();
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        TextEditor     editor  = new TextEditor();
        CommandHistory history = new CommandHistory();

        System.out.println("--- Executing commands ---");
        history.execute(new InsertCommand(editor, "Hello"));
        history.execute(new InsertCommand(editor, ", World"));
        history.execute(new DeleteCommand(editor, 6));   // removes ", World"

        System.out.println("\n--- Undoing last 2 commands ---");
        history.undo(); // re-inserts ", World"
        history.undo(); // removes ", World" again? No — undoes InsertCommand(", World") → deletes it

        System.out.println("\nFinal text: \"" + editor.getText() + "\"");
    }
}
