package structural.decorator;

/**
 * Decorator Pattern
 *
 * Intent: Attach additional responsibilities to an object dynamically.
 * Provides a flexible alternative to subclassing for extending functionality.
 *
 * Each decorator wraps another component, adds its own behaviour, and still
 * fulfils the same interface — decorators can be stacked in any combination.
 */

// ── Component interface ──────────────────────────────────────────────────────

/** The core interface: a beverage has a description and a cost. */
interface Coffee {
    String getDescription();
    double getCost();
}

// ── Concrete Component ────────────────────────────────────────────────────────

/** The base beverage — a plain espresso. */
class Espresso implements Coffee {
    @Override public String getDescription() { return "Espresso"; }
    @Override public double getCost()        { return 1.00; }
}

// ── Base Decorator ────────────────────────────────────────────────────────────

/**
 * Abstract decorator: wraps a Coffee and delegates to it.
 * Concrete decorators extend this and add their extra behaviour
 * before/after the delegation call.
 */
abstract class CoffeeDecorator implements Coffee {
    /** The wrapped component — could be a base coffee or another decorator. */
    protected final Coffee wrapped;

    CoffeeDecorator(Coffee coffee) { this.wrapped = coffee; }

    @Override public String getDescription() { return wrapped.getDescription(); }
    @Override public double getCost()        { return wrapped.getCost(); }
}

// ── Concrete Decorators ───────────────────────────────────────────────────────

class Milk extends CoffeeDecorator {
    Milk(Coffee coffee) { super(coffee); }

    @Override public String getDescription() { return wrapped.getDescription() + ", Milk"; }
    @Override public double getCost()        { return wrapped.getCost() + 0.25; }
}

class Sugar extends CoffeeDecorator {
    Sugar(Coffee coffee) { super(coffee); }

    @Override public String getDescription() { return wrapped.getDescription() + ", Sugar"; }
    @Override public double getCost()        { return wrapped.getCost() + 0.10; }
}

class WhippedCream extends CoffeeDecorator {
    WhippedCream(Coffee coffee) { super(coffee); }

    @Override public String getDescription() { return wrapped.getDescription() + ", Whipped Cream"; }
    @Override public double getCost()        { return wrapped.getCost() + 0.50; }
}

class VanillaSyrup extends CoffeeDecorator {
    VanillaSyrup(Coffee coffee) { super(coffee); }

    @Override public String getDescription() { return wrapped.getDescription() + ", Vanilla Syrup"; }
    @Override public double getCost()        { return wrapped.getCost() + 0.35; }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Plain espresso
        Coffee order1 = new Espresso();
        printOrder(order1);

        // Espresso + Milk + Sugar — decorators stack like Russian dolls
        Coffee order2 = new Sugar(new Milk(new Espresso()));
        printOrder(order2);

        // Fully loaded: Espresso + Milk + Whipped Cream + Vanilla Syrup + extra Sugar
        Coffee order3 = new Sugar(
                            new VanillaSyrup(
                                new WhippedCream(
                                    new Milk(
                                        new Espresso()))));
        printOrder(order3);
    }

    private static void printOrder(Coffee coffee) {
        System.out.printf("%-55s $%.2f%n", coffee.getDescription(), coffee.getCost());
    }
}
