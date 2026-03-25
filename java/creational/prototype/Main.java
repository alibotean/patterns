package creational.prototype;

/**
 * Prototype Pattern
 *
 * Intent: Specify the kinds of objects to create using a prototypical instance,
 * and create new objects by copying (cloning) this prototype.
 *
 * Use when: Object creation is expensive (e.g., DB round-trip, complex init) and
 * you need many similar objects — clone a pre-built prototype instead.
 */

// ── Prototype interface ──────────────────────────────────────────────────────

/** All shapes can clone themselves — the client never calls new directly. */
interface Shape {
    Shape clone();
    void draw();
}

// ── Concrete Prototypes ──────────────────────────────────────────────────────

class Circle implements Shape {
    private int x, y;
    private int radius;
    private String color;

    Circle(int x, int y, int radius, String color) {
        this.x = x; this.y = y; this.radius = radius; this.color = color;
    }

    /** Copy constructor used by clone(). */
    private Circle(Circle source) {
        this(source.x, source.y, source.radius, source.color);
    }

    public void setPosition(int x, int y) { this.x = x; this.y = y; }

    /**
     * Returns a new Circle with the same field values.
     * The caller can then tweak just the fields that differ.
     */
    @Override
    public Shape clone() { return new Circle(this); }

    @Override
    public void draw() {
        System.out.printf("Circle  color=%-8s radius=%d at (%d,%d)%n", color, radius, x, y);
    }
}

class Rectangle implements Shape {
    private int x, y;
    private int width, height;
    private String color;

    Rectangle(int x, int y, int width, int height, String color) {
        this.x = x; this.y = y; this.width = width; this.height = height; this.color = color;
    }

    private Rectangle(Rectangle source) {
        this(source.x, source.y, source.width, source.height, source.color);
    }

    public void setPosition(int x, int y) { this.x = x; this.y = y; }

    @Override
    public Shape clone() { return new Rectangle(this); }

    @Override
    public void draw() {
        System.out.printf("Rect    color=%-8s %dx%d at (%d,%d)%n", color, width, height, x, y);
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // ── Prototype instances (imagine these were expensive to create) ──
        Circle    redCircle = new Circle(0, 0, 50, "red");
        Rectangle blueRect  = new Rectangle(0, 0, 100, 60, "blue");

        System.out.println("Originals:");
        redCircle.draw();
        blueRect.draw();

        // Clone and place copies at different positions — no need to repeat
        // constructor arguments for color/size/radius that stay the same.
        Circle copy1 = (Circle) redCircle.clone();
        copy1.setPosition(100, 200);

        Circle copy2 = (Circle) redCircle.clone();
        copy2.setPosition(300, 400);

        Rectangle copy3 = (Rectangle) blueRect.clone();
        copy3.setPosition(50, 50);

        System.out.println("\nClones:");
        copy1.draw();
        copy2.draw();
        copy3.draw();

        // Verify clones are independent objects
        System.out.println("\nAre originals and clones distinct objects?");
        System.out.println("redCircle != copy1 : " + (redCircle != copy1)); // true
    }
}
