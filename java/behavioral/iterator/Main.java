package behavioral.iterator;

import java.util.NoSuchElementException;

/**
 * Iterator Pattern
 *
 * Intent: Provide a way to access the elements of an aggregate object sequentially
 * without exposing its underlying representation.
 *
 * Use when: You want a uniform traversal interface regardless of how the collection
 * is stored internally (array, linked list, tree, etc.).
 *
 * This example implements a bounded, type-safe stack with its own iterator —
 * the internal array is never leaked to clients.
 */

// ── Iterator interface ────────────────────────────────────────────────────────

interface Iterator<T> {
    boolean hasNext();
    T next();
}

// ── Aggregate interface ───────────────────────────────────────────────────────

/** Any collection that can produce an iterator implements this. */
interface IterableCollection<T> {
    Iterator<T> createIterator();
    int size();
}

// ── Concrete Aggregate ────────────────────────────────────────────────────────

/**
 * A simple fixed-capacity stack backed by an array.
 * Clients never see the internal array — they traverse via an Iterator.
 */
class BoundedStack<T> implements IterableCollection<T> {
    private final Object[] data;
    private int top = -1;

    BoundedStack(int capacity) { data = new Object[capacity]; }

    public void push(T item) {
        if (top == data.length - 1) throw new IllegalStateException("Stack is full");
        data[++top] = item;
    }

    @Override public int size() { return top + 1; }

    /**
     * Returns an iterator that traverses from bottom to top (FIFO order).
     * The iterator is an anonymous class with access to the private array —
     * but the array itself is never exposed to external callers.
     */
    @Override
    public Iterator<T> createIterator() {
        return new Iterator<T>() {
            private int index = 0; // starts at bottom of stack

            @Override
            public boolean hasNext() { return index <= top; }

            @Override
            @SuppressWarnings("unchecked")
            public T next() {
                if (!hasNext()) throw new NoSuchElementException();
                return (T) data[index++];
            }
        };
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        BoundedStack<String> stack = new BoundedStack<>(5);
        stack.push("first");
        stack.push("second");
        stack.push("third");

        System.out.println("Traversing the stack (bottom → top):");
        Iterator<String> it = stack.createIterator();
        while (it.hasNext()) {
            System.out.println("  " + it.next());
        }

        // The internal array is never accessible — callers can only iterate
        System.out.println("\nStack size: " + stack.size());
    }
}
