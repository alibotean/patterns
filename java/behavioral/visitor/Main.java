package behavioral.visitor;

/**
 * Visitor Pattern
 *
 * Intent: Represent an operation to be performed on elements of an object structure.
 * Lets you define a new operation without changing the classes of the elements it operates on.
 *
 * Use when: You need to perform many distinct, unrelated operations on an object structure
 * and you don't want to "pollute" those classes with these operations.
 *
 * The key mechanism is double dispatch:
 *   visitor.visit(element) is resolved to the right overload via element.accept(visitor).
 */

// ── Element interface ─────────────────────────────────────────────────────────

/**
 * Each element in the structure accepts a visitor.
 * accept() calls back the visitor with a reference to itself — this is double dispatch.
 */
interface Shape {
    void accept(ShapeVisitor visitor);
}

// ── Concrete Elements ─────────────────────────────────────────────────────────

class Circle implements Shape {
    final double radius;
    Circle(double radius) { this.radius = radius; }

    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this); // dispatches to visit(Circle)
    }
}

class Rectangle implements Shape {
    final double width, height;
    Rectangle(double width, double height) { this.width = width; this.height = height; }

    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this); // dispatches to visit(Rectangle)
    }
}

class Triangle implements Shape {
    final double base, height;
    Triangle(double base, double height) { this.base = base; this.height = height; }

    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this); // dispatches to visit(Triangle)
    }
}

// ── Visitor interface ─────────────────────────────────────────────────────────

/**
 * One overload per concrete element type.
 * Adding a new operation means adding a new Visitor — not touching the Shape classes.
 */
interface ShapeVisitor {
    void visit(Circle circle);
    void visit(Rectangle rectangle);
    void visit(Triangle triangle);
}

// ── Concrete Visitors ─────────────────────────────────────────────────────────

/** Computes the area of each shape. */
class AreaCalculator implements ShapeVisitor {
    private double totalArea = 0;

    @Override public void visit(Circle c)    { totalArea += Math.PI * c.radius * c.radius; }
    @Override public void visit(Rectangle r) { totalArea += r.width * r.height; }
    @Override public void visit(Triangle t)  { totalArea += 0.5 * t.base * t.height; }

    public double getTotalArea() { return totalArea; }
}

/** Produces a human-readable description of each shape. */
class ShapeDescriber implements ShapeVisitor {
    @Override
    public void visit(Circle c) {
        System.out.printf("Circle    radius=%.1f  area=%.2f%n", c.radius, Math.PI * c.radius * c.radius);
    }
    @Override
    public void visit(Rectangle r) {
        System.out.printf("Rectangle %.1fx%.1f  area=%.2f%n", r.width, r.height, r.width * r.height);
    }
    @Override
    public void visit(Triangle t) {
        System.out.printf("Triangle  base=%.1f height=%.1f  area=%.2f%n", t.base, t.height, 0.5 * t.base * t.height);
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        Shape[] shapes = {
            new Circle(5),
            new Rectangle(4, 6),
            new Triangle(3, 8),
            new Circle(2),
        };

        // Apply the "describe" operation — shapes are unchanged
        System.out.println("=== Shape descriptions ===");
        ShapeDescriber describer = new ShapeDescriber();
        for (Shape s : shapes) s.accept(describer);

        // Apply the "area" operation — same shapes, different visitor, no class modification
        System.out.println("\n=== Area totals ===");
        AreaCalculator calc = new AreaCalculator();
        for (Shape s : shapes) s.accept(calc);
        System.out.printf("Total area of all shapes: %.2f%n", calc.getTotalArea());
    }
}
