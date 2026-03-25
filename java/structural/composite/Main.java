package structural.composite;

import java.util.ArrayList;
import java.util.List;

/**
 * Composite Pattern
 *
 * Intent: Compose objects into tree structures to represent part-whole hierarchies.
 * Lets clients treat individual objects and compositions uniformly.
 *
 * Classic example: a file system where a Folder contains Files and other Folders,
 * but both respond to the same operations (e.g., getSize(), print()).
 */

// ── Component interface ──────────────────────────────────────────────────────

/**
 * The common interface for both leaves (File) and composites (Folder).
 * The client only ever holds a FileSystemItem — it doesn't need to distinguish.
 */
interface FileSystemItem {
    String getName();
    long   getSize(); // bytes
    void   print(String indent);
}

// ── Leaf ─────────────────────────────────────────────────────────────────────

/**
 * A leaf node — has no children.
 * Implements every operation directly.
 */
class File implements FileSystemItem {
    private final String name;
    private final long   size;

    File(String name, long size) {
        this.name = name;
        this.size = size;
    }

    @Override public String getName()  { return name; }
    @Override public long   getSize()  { return size; }

    @Override
    public void print(String indent) {
        System.out.printf("%s📄 %s (%d B)%n", indent, name, size);
    }
}

// ── Composite ────────────────────────────────────────────────────────────────

/**
 * A composite node — holds child FileSystemItems (files or other folders).
 * getSize() and print() delegate to children recursively.
 */
class Folder implements FileSystemItem {
    private final String               name;
    private final List<FileSystemItem> children = new ArrayList<>();

    Folder(String name) { this.name = name; }

    /** Add any FileSystemItem — could be a File or another Folder. */
    public void add(FileSystemItem item) { children.add(item); }

    @Override public String getName() { return name; }

    /** Size is the sum of all children's sizes — recursion handles nested folders. */
    @Override
    public long getSize() {
        return children.stream().mapToLong(FileSystemItem::getSize).sum();
    }

    @Override
    public void print(String indent) {
        System.out.printf("%s📁 %s/ (%d B total)%n", indent, name, getSize());
        // Each child prints itself — the client doesn't need to know if it's a file or folder
        for (FileSystemItem child : children) {
            child.print(indent + "  ");
        }
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Build a small tree
        Folder root = new Folder("root");

        Folder src = new Folder("src");
        src.add(new File("Main.java",  1200));
        src.add(new File("Utils.java",  800));

        Folder resources = new Folder("resources");
        resources.add(new File("config.yml", 300));
        resources.add(new File("logo.png",  45000));

        root.add(src);
        root.add(resources);
        root.add(new File("README.md", 2500));

        // The client calls print() on root — composite handles the recursion
        root.print("");

        System.out.println("\nTotal project size: " + root.getSize() + " B");
    }
}
