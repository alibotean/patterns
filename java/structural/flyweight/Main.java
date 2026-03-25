package structural.flyweight;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * Flyweight Pattern
 *
 * Intent: Use sharing to support large numbers of fine-grained objects efficiently.
 *
 * Key idea: split object state into:
 *   • Intrinsic state — shared, immutable (stored in the flyweight)
 *   • Extrinsic state — unique per context, passed in at runtime
 *
 * Use when: You must create millions of similar objects and memory is a concern.
 * Classic example: characters in a text editor, particles in a game, trees in a forest.
 */

// ── Flyweight (intrinsic state) ───────────────────────────────────────────────

/**
 * Stores only the intrinsic (shared) state of a tree type:
 * mesh, texture, and color — all identical trees of the same species share one object.
 */
class TreeType {
    private final String name;    // e.g. "Oak"
    private final String color;   // e.g. "#228B22"
    private final String texture; // e.g. "oak_bark.png"

    TreeType(String name, String color, String texture) {
        this.name = name; this.color = color; this.texture = texture;
    }

    /**
     * Draws the tree using its shared state PLUS the extrinsic state
     * (x, y position) that is passed in — NOT stored in this object.
     */
    public void draw(int x, int y) {
        System.out.printf("Drawing %s tree [%s, %s] at (%d, %d)%n",
                          name, color, texture, x, y);
    }
}

// ── Flyweight Factory ────────────────────────────────────────────────────────

/**
 * Creates and caches TreeType flyweights.
 * Returns the existing instance when the same species is requested again —
 * never allocates a duplicate.
 */
class TreeFactory {
    private static final Map<String, TreeType> cache = new HashMap<>();

    public static TreeType getTreeType(String name, String color, String texture) {
        String key = name + "|" + color + "|" + texture;
        // Only create a new flyweight if this species hasn't been seen before
        return cache.computeIfAbsent(key, k -> {
            System.out.println("[Factory] Creating new TreeType: " + name);
            return new TreeType(name, color, texture);
        });
    }

    public static int getCachedCount() { return cache.size(); }
}

// ── Context (extrinsic state) ────────────────────────────────────────────────

/**
 * Represents one tree in the forest.
 * Stores only the unique, context-specific state (x, y) and holds a
 * reference to the shared TreeType flyweight — NOT a copy of it.
 */
class Tree {
    private final int      x, y;      // extrinsic — unique per tree instance
    private final TreeType type;      // intrinsic — shared flyweight

    Tree(int x, int y, TreeType type) {
        this.x = x; this.y = y; this.type = type;
    }

    public void draw() {
        type.draw(x, y); // pass extrinsic state into the flyweight
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        Random rng   = new Random(42);
        Tree[] forest = new Tree[10];

        // Plant 10 trees of only 3 species — the factory reuses flyweights
        String[][] species = {
            {"Oak",    "#228B22", "oak_bark.png"},
            {"Pine",   "#006400", "pine_bark.png"},
            {"Birch",  "#F5F5DC", "birch_bark.png"},
        };

        for (int i = 0; i < forest.length; i++) {
            String[] s = species[i % species.length];
            TreeType type = TreeFactory.getTreeType(s[0], s[1], s[2]);
            forest[i] = new Tree(rng.nextInt(1000), rng.nextInt(1000), type);
        }

        System.out.println("\n--- Drawing forest ---");
        for (Tree t : forest) t.draw();

        System.out.println("\nTotal trees: " + forest.length);
        System.out.println("Unique TreeType objects in memory: " + TreeFactory.getCachedCount());
        // 10 trees, but only 3 TreeType objects — the flyweights are shared
    }
}
