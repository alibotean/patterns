package behavioral.observer;

import java.util.ArrayList;
import java.util.List;

/**
 * Observer Pattern  (also known as Publish-Subscribe)
 *
 * Intent: Define a one-to-many dependency between objects so that when one object
 * changes state, all its dependents are notified and updated automatically.
 *
 * Use when: Changes to one object require changing an unknown number of others,
 * or you want to decouple the source of events from the things that react to them.
 */

// ── Observer interface ────────────────────────────────────────────────────────

/** Any class that wants notifications implements this. */
interface Observer {
    /**
     * Called by the subject whenever its state changes.
     *
     * @param ticker  the stock symbol that changed
     * @param price   the new price
     */
    void update(String ticker, double price);
}

// ── Subject interface ─────────────────────────────────────────────────────────

interface Subject {
    void subscribe(Observer observer);
    void unsubscribe(Observer observer);
    void notifyObservers();
}

// ── Concrete Subject ──────────────────────────────────────────────────────────

/**
 * A stock ticker that broadcasts price changes to all registered observers.
 * It knows nothing about the concrete observer classes.
 */
class StockMarket implements Subject {
    private final List<Observer> observers = new ArrayList<>();
    private String ticker;
    private double price;

    @Override public void subscribe(Observer o)   { observers.add(o); }
    @Override public void unsubscribe(Observer o) { observers.remove(o); }

    @Override
    public void notifyObservers() {
        for (Observer o : observers) {
            o.update(ticker, price);  // push the changed data to each observer
        }
    }

    /** Updates the price and automatically notifies all subscribers. */
    public void setPrice(String ticker, double price) {
        this.ticker = ticker;
        this.price  = price;
        System.out.printf("%n[StockMarket] %s price changed to $%.2f%n", ticker, price);
        notifyObservers();
    }
}

// ── Concrete Observers ────────────────────────────────────────────────────────

/** A display panel that shows the current stock price. */
class StockDisplay implements Observer {
    private final String name;

    StockDisplay(String name) { this.name = name; }

    @Override
    public void update(String ticker, double price) {
        System.out.printf("  [%s] %s → $%.2f%n", name, ticker, price);
    }
}

/** An alert system that triggers only when the price exceeds a threshold. */
class PriceAlert implements Observer {
    private final String name;
    private final double threshold;

    PriceAlert(String name, double threshold) {
        this.name      = name;
        this.threshold = threshold;
    }

    @Override
    public void update(String ticker, double price) {
        if (price >= threshold) {
            System.out.printf("  [ALERT — %s] %s hit $%.2f (threshold: $%.2f)!%n",
                              name, ticker, price, threshold);
        }
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        StockMarket market = new StockMarket();

        Observer display1 = new StockDisplay("Main Board");
        Observer display2 = new StockDisplay("Mobile App");
        Observer alert    = new PriceAlert("High-Price Alert", 200.00);

        market.subscribe(display1);
        market.subscribe(display2);
        market.subscribe(alert);

        market.setPrice("ACME", 150.00);
        market.setPrice("ACME", 195.50);
        market.setPrice("ACME", 210.00); // triggers the alert

        // Unsubscribe one display — subsequent updates skip it
        System.out.println("\n[Unsubscribing Mobile App]");
        market.unsubscribe(display2);
        market.setPrice("ACME", 220.00);
    }
}
