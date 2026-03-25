package creational.abstract_factory;

/**
 * Abstract Factory Pattern
 *
 * Intent: Provide an interface for creating families of related or dependent objects
 * without specifying their concrete classes.
 *
 * Key difference from Factory Method: Abstract Factory produces a *family* of products
 * that must be used together (e.g., all Windows widgets or all Mac widgets).
 */

// ── Abstract Products ────────────────────────────────────────────────────────

/** Abstract product: Button */
interface Button {
    void render();
    void onClick();
}

/** Abstract product: Checkbox */
interface Checkbox {
    void render();
    void toggle();
}

// ── Concrete Products — Windows family ──────────────────────────────────────

class WindowsButton implements Button {
    @Override public void render()  { System.out.println("[Windows] Rendering a flat, square button"); }
    @Override public void onClick() { System.out.println("[Windows] Button clicked — plays Windows click sound"); }
}

class WindowsCheckbox implements Checkbox {
    @Override public void render()  { System.out.println("[Windows] Rendering a square checkbox"); }
    @Override public void toggle()  { System.out.println("[Windows] Checkbox toggled — shows checkmark"); }
}

// ── Concrete Products — macOS family ────────────────────────────────────────

class MacButton implements Button {
    @Override public void render()  { System.out.println("[macOS] Rendering a rounded, gradient button"); }
    @Override public void onClick() { System.out.println("[macOS] Button clicked — plays Mac click sound"); }
}

class MacCheckbox implements Checkbox {
    @Override public void render()  { System.out.println("[macOS] Rendering a rounded checkbox"); }
    @Override public void toggle()  { System.out.println("[macOS] Checkbox toggled — shows blue tick"); }
}

// ── Abstract Factory ─────────────────────────────────────────────────────────

/**
 * Declares creation methods for each distinct product in the family.
 * Concrete factories implement this to produce a consistent set of widgets.
 */
interface UIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// ── Concrete Factories ───────────────────────────────────────────────────────

/** Produces the Windows family — every product is a Windows variant. */
class WindowsFactory implements UIFactory {
    @Override public Button   createButton()   { return new WindowsButton(); }
    @Override public Checkbox createCheckbox() { return new WindowsCheckbox(); }
}

/** Produces the macOS family — every product is a Mac variant. */
class MacFactory implements UIFactory {
    @Override public Button   createButton()   { return new MacButton(); }
    @Override public Checkbox createCheckbox() { return new MacCheckbox(); }
}

// ── Client ───────────────────────────────────────────────────────────────────

/**
 * The Application only talks to the abstract factory and abstract products.
 * It never references Windows- or Mac-specific classes — swapping the factory
 * at construction time is all it takes to change the entire UI toolkit.
 */
class Application {
    private final Button   button;
    private final Checkbox checkbox;

    Application(UIFactory factory) {
        // Products are created via the factory — Application doesn't know their concrete types
        this.button   = factory.createButton();
        this.checkbox = factory.createCheckbox();
    }

    public void renderUI() {
        button.render();
        checkbox.render();
    }

    public void interactUI() {
        button.onClick();
        checkbox.toggle();
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Normally determined at runtime (OS detection, config, etc.)
        UIFactory factory = detectFactory();

        Application app = new Application(factory);
        app.renderUI();
        System.out.println("--- user interaction ---");
        app.interactUI();
    }

    /** Simulates picking the right factory based on the operating system. */
    private static UIFactory detectFactory() {
        String os = System.getProperty("os.name", "").toLowerCase();
        if (os.contains("mac")) {
            System.out.println("Detected macOS — using MacFactory\n");
            return new MacFactory();
        }
        System.out.println("Detected Windows/Other — using WindowsFactory\n");
        return new WindowsFactory();
    }
}
