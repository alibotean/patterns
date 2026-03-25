package structural.bridge;

/**
 * Bridge Pattern
 *
 * Intent: Decouple an abstraction from its implementation so the two can vary independently.
 *
 * Without Bridge: adding a new shape AND a new renderer would require N×M subclasses.
 * With Bridge: shapes and renderers grow independently — just N + M classes.
 *
 * The "bridge" is the reference the abstraction holds to the implementor.
 */

// ── Implementor interface ────────────────────────────────────────────────────

/**
 * Defines the low-level rendering operations.
 * Shapes delegate to this instead of doing rendering themselves.
 */
interface Renderer {
    void renderCircle(int x, int y, int radius);
    void renderRectangle(int x, int y, int width, int height);
}

// ── Concrete Implementors ────────────────────────────────────────────────────

class VectorRenderer implements Renderer {
    @Override
    public void renderCircle(int x, int y, int radius) {
        System.out.printf("Vector: drawing circle at (%d,%d) r=%d%n", x, y, radius);
    }
    @Override
    public void renderRectangle(int x, int y, int width, int height) {
        System.out.printf("Vector: drawing rect   at (%d,%d) %dx%d%n", x, y, width, height);
    }
}

class RasterRenderer implements Renderer {
    @Override
    public void renderCircle(int x, int y, int radius) {
        System.out.printf("Raster: pixelating circle at (%d,%d) r=%d%n", x, y, radius);
    }
    @Override
    public void renderRectangle(int x, int y, int width, int height) {
        System.out.printf("Raster: pixelating rect   at (%d,%d) %dx%d%n", x, y, width, height);
    }
}

// ── Abstraction ──────────────────────────────────────────────────────────────

/**
 * The abstraction layer. Holds a reference (the bridge) to a Renderer.
 * Shape subclasses implement draw() using whichever Renderer was injected.
 */
abstract class Shape {
    /** The bridge — can be any Renderer implementation. */
    protected final Renderer renderer;

    Shape(Renderer renderer) {
        this.renderer = renderer;
    }

    public abstract void draw();
}

// ── Refined Abstractions ─────────────────────────────────────────────────────

class Circle extends Shape {
    private final int x, y, radius;

    Circle(int x, int y, int radius, Renderer renderer) {
        super(renderer);
        this.x = x; this.y = y; this.radius = radius;
    }

    @Override
    public void draw() {
        // Shape knows *what* to draw; the renderer knows *how*
        renderer.renderCircle(x, y, radius);
    }
}

class Rectangle extends Shape {
    private final int x, y, width, height;

    Rectangle(int x, int y, int width, int height, Renderer renderer) {
        super(renderer);
        this.x = x; this.y = y; this.width = width; this.height = height;
    }

    @Override
    public void draw() {
        renderer.renderRectangle(x, y, width, height);
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        Renderer vector = new VectorRenderer();
        Renderer raster = new RasterRenderer();

        // Same shape hierarchy, different renderers — no explosion of subclasses
        Shape[] shapes = {
            new Circle(10, 20, 5, vector),
            new Circle(30, 40, 8, raster),
            new Rectangle(5, 5, 100, 50, vector),
            new Rectangle(5, 5, 100, 50, raster),
        };

        for (Shape shape : shapes) {
            shape.draw();
        }
    }
}
