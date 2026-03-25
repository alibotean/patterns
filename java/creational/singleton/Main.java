package creational.singleton;

/**
 * Singleton Pattern
 *
 * Intent: Ensure a class has only one instance and provide a global access point to it.
 * Use when: Exactly one object is needed to coordinate actions across the system
 * (e.g., a logger, configuration manager, or connection pool).
 */

/**
 * The Singleton class holds a single static instance of itself.
 * All access goes through getInstance(), which creates the instance on first call
 * and returns the same one on every subsequent call.
 *
 * Thread-safe via double-checked locking.
 */
class AppLogger {

    // The sole instance — volatile ensures visibility across threads
    private static volatile AppLogger instance;

    private int messageCount = 0;

    // Private constructor prevents direct instantiation from outside
    private AppLogger() {
        System.out.println("[AppLogger] Logger created.");
    }

    /**
     * Returns the single instance, creating it lazily on the first call.
     * Double-checked locking avoids synchronization overhead after initialization.
     */
    public static AppLogger getInstance() {
        if (instance == null) {
            synchronized (AppLogger.class) {
                if (instance == null) {
                    instance = new AppLogger();
                }
            }
        }
        return instance;
    }

    /** Logs a message and keeps a running count. */
    public void log(String message) {
        messageCount++;
        System.out.printf("[LOG #%d] %s%n", messageCount, message);
    }

    public int getMessageCount() {
        return messageCount;
    }
}

public class Main {
    public static void main(String[] args) {
        // Both variables point to the exact same object
        AppLogger logger1 = AppLogger.getInstance();
        AppLogger logger2 = AppLogger.getInstance();

        logger1.log("Application started");
        logger2.log("User logged in");
        logger1.log("Processing request");

        System.out.println("\nSame instance? " + (logger1 == logger2));       // true
        System.out.println("Total messages logged: " + logger2.getMessageCount()); // 3
    }
}
