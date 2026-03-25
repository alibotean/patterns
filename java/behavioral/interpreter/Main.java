package behavioral.interpreter;

import java.util.HashMap;
import java.util.Map;

/**
 * Interpreter Pattern
 *
 * Intent: Given a language, define a representation for its grammar along with an
 * interpreter that uses the representation to interpret sentences in the language.
 *
 * Use when: You have a simple, well-defined grammar that needs to be evaluated
 * repeatedly (e.g., expression evaluators, rule engines, template parsers).
 *
 * This example interprets simple arithmetic expressions with variables:
 *   "x + 3", "a - b", "2 + x"
 */

// ── Context ──────────────────────────────────────────────────────────────────

/** Holds variable bindings used during interpretation. */
class Context {
    private final Map<String, Integer> variables = new HashMap<>();

    public void set(String name, int value) { variables.put(name, value); }

    public int get(String name) {
        if (!variables.containsKey(name))
            throw new IllegalArgumentException("Undefined variable: " + name);
        return variables.get(name);
    }
}

// ── Abstract Expression ───────────────────────────────────────────────────────

/** Every node in the AST can interpret itself given a context. */
interface Expression {
    int interpret(Context context);
}

// ── Terminal Expressions ──────────────────────────────────────────────────────

/** A literal integer — just returns itself. */
class NumberExpression implements Expression {
    private final int number;

    NumberExpression(int number) { this.number = number; }

    @Override
    public int interpret(Context context) { return number; }
}

/** A variable — looks up its value in the context. */
class VariableExpression implements Expression {
    private final String name;

    VariableExpression(String name) { this.name = name; }

    @Override
    public int interpret(Context context) { return context.get(name); }
}

// ── Non-Terminal Expressions (grammar rules) ─────────────────────────────────

/** Represents: left + right */
class AddExpression implements Expression {
    private final Expression left, right;

    AddExpression(Expression left, Expression right) {
        this.left = left; this.right = right;
    }

    @Override
    public int interpret(Context context) {
        return left.interpret(context) + right.interpret(context);
    }
}

/** Represents: left - right */
class SubtractExpression implements Expression {
    private final Expression left, right;

    SubtractExpression(Expression left, Expression right) {
        this.left = left; this.right = right;
    }

    @Override
    public int interpret(Context context) {
        return left.interpret(context) - right.interpret(context);
    }
}

/** Represents: left * right */
class MultiplyExpression implements Expression {
    private final Expression left, right;

    MultiplyExpression(Expression left, Expression right) {
        this.left = left; this.right = right;
    }

    @Override
    public int interpret(Context context) {
        return left.interpret(context) * right.interpret(context);
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        Context ctx = new Context();
        ctx.set("x", 10);
        ctx.set("y", 4);

        // Build AST for:  (x + y) * 2 - 3
        //
        //         SubtractExpression
        //        /                  \
        //   MultiplyExpression      NumberExpression(3)
        //   /           \
        //  AddExpression  NumberExpression(2)
        //  /        \
        // Var(x)   Var(y)

        Expression expr =
            new SubtractExpression(
                new MultiplyExpression(
                    new AddExpression(
                        new VariableExpression("x"),
                        new VariableExpression("y")
                    ),
                    new NumberExpression(2)
                ),
                new NumberExpression(3)
            );

        int result = expr.interpret(ctx);
        System.out.println("(x + y) * 2 - 3  where x=10, y=4");
        System.out.println("= (" + ctx.get("x") + " + " + ctx.get("y") + ") * 2 - 3");
        System.out.println("= " + result);  // (10+4)*2-3 = 25
    }
}
