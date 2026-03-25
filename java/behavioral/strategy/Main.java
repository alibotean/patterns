package behavioral.strategy;

import java.util.Arrays;

/**
 * Strategy Pattern
 *
 * Intent: Define a family of algorithms, encapsulate each one, and make them
 * interchangeable. The algorithm can vary independently from the clients that use it.
 *
 * Use when: You have multiple variants of an algorithm and want to switch between them
 * at runtime without rewriting the class that uses them.
 */

// ── Strategy interface ────────────────────────────────────────────────────────

/** A sorting strategy that sorts an integer array in-place. */
interface SortStrategy {
    void sort(int[] data);
    String name();
}

// ── Concrete Strategies ───────────────────────────────────────────────────────

/** Bubble sort — O(n²), simple to understand. */
class BubbleSort implements SortStrategy {
    @Override
    public void sort(int[] data) {
        int n = data.length;
        for (int i = 0; i < n - 1; i++)
            for (int j = 0; j < n - i - 1; j++)
                if (data[j] > data[j + 1]) {
                    int tmp = data[j]; data[j] = data[j + 1]; data[j + 1] = tmp;
                }
    }
    @Override public String name() { return "BubbleSort"; }
}

/** Insertion sort — O(n²) worst case, but O(n) on nearly-sorted data. */
class InsertionSort implements SortStrategy {
    @Override
    public void sort(int[] data) {
        for (int i = 1; i < data.length; i++) {
            int key = data[i], j = i - 1;
            while (j >= 0 && data[j] > key) { data[j + 1] = data[j]; j--; }
            data[j + 1] = key;
        }
    }
    @Override public String name() { return "InsertionSort"; }
}

/** Delegates to Java's built-in Arrays.sort — O(n log n). */
class JavaBuiltinSort implements SortStrategy {
    @Override
    public void sort(int[] data) { Arrays.sort(data); }
    @Override public String name() { return "Arrays.sort (Timsort)"; }
}

// ── Context ───────────────────────────────────────────────────────────────────

/**
 * The Sorter context is decoupled from any specific algorithm.
 * Swap the strategy at construction time or at runtime — nothing else changes.
 */
class Sorter {
    private SortStrategy strategy;

    Sorter(SortStrategy strategy) { this.strategy = strategy; }

    /** Swap the algorithm at runtime. */
    public void setStrategy(SortStrategy strategy) { this.strategy = strategy; }

    public int[] sort(int[] data) {
        int[] copy = Arrays.copyOf(data, data.length); // don't mutate the original
        strategy.sort(copy);
        System.out.printf("%-30s %s%n", strategy.name() + ":", Arrays.toString(copy));
        return copy;
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        int[] data = {5, 3, 8, 1, 9, 2, 7, 4, 6};
        System.out.println("Input: " + Arrays.toString(data));
        System.out.println();

        Sorter sorter = new Sorter(new BubbleSort());
        sorter.sort(data);

        // Swap strategy at runtime — same Sorter, different algorithm
        sorter.setStrategy(new InsertionSort());
        sorter.sort(data);

        sorter.setStrategy(new JavaBuiltinSort());
        sorter.sort(data);
    }
}
