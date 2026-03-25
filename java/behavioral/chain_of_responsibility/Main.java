package behavioral.chain_of_responsibility;

/**
 * Chain of Responsibility Pattern
 *
 * Intent: Avoid coupling the sender of a request to its receiver by giving multiple
 * objects a chance to handle it. Chain the handlers and pass the request along until
 * one handles it.
 *
 * Use when: The handler isn't known ahead of time, or several objects may handle a
 * request (e.g., support tiers, middleware pipelines, event bubbling).
 */

// ── Handler interface ────────────────────────────────────────────────────────

/**
 * Each handler knows its successor. If it can't handle a request, it forwards it.
 */
abstract class SupportHandler {
    protected SupportHandler next;

    /** Fluent setter — lets you chain handlers: lvl1.setNext(lvl2).setNext(lvl3). */
    public SupportHandler setNext(SupportHandler next) {
        this.next = next;
        return next;
    }

    /**
     * Attempt to handle the ticket. If this handler can't, pass it to the next one.
     * Returns true if the ticket was ultimately handled, false otherwise.
     */
    public abstract boolean handle(SupportTicket ticket);
}

// ── Request ──────────────────────────────────────────────────────────────────

/** Severity levels from lowest to highest. */
enum Severity { LOW, MEDIUM, HIGH, CRITICAL }

class SupportTicket {
    final String   description;
    final Severity severity;

    SupportTicket(String description, Severity severity) {
        this.description = description;
        this.severity    = severity;
    }

    @Override
    public String toString() {
        return String.format("[%s] %s", severity, description);
    }
}

// ── Concrete Handlers ────────────────────────────────────────────────────────

/** Tier 1: handles only low-severity tickets. */
class Level1Support extends SupportHandler {
    @Override
    public boolean handle(SupportTicket ticket) {
        if (ticket.severity == Severity.LOW) {
            System.out.println("Level 1 Support resolved: " + ticket);
            return true;
        }
        System.out.println("Level 1 cannot handle " + ticket.severity + " — escalating...");
        return next != null && next.handle(ticket);
    }
}

/** Tier 2: handles medium severity. */
class Level2Support extends SupportHandler {
    @Override
    public boolean handle(SupportTicket ticket) {
        if (ticket.severity == Severity.MEDIUM) {
            System.out.println("Level 2 Support resolved: " + ticket);
            return true;
        }
        System.out.println("Level 2 cannot handle " + ticket.severity + " — escalating...");
        return next != null && next.handle(ticket);
    }
}

/** Tier 3: handles high severity. */
class Level3Support extends SupportHandler {
    @Override
    public boolean handle(SupportTicket ticket) {
        if (ticket.severity == Severity.HIGH) {
            System.out.println("Level 3 Support resolved: " + ticket);
            return true;
        }
        System.out.println("Level 3 cannot handle " + ticket.severity + " — escalating...");
        return next != null && next.handle(ticket);
    }
}

/** Executive team: handles critical incidents. */
class ExecutiveSupport extends SupportHandler {
    @Override
    public boolean handle(SupportTicket ticket) {
        // Terminal handler — takes anything, no further escalation
        System.out.println("Executive team resolved: " + ticket);
        return true;
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Build the chain: L1 → L2 → L3 → Executive
        SupportHandler l1 = new Level1Support();
        l1.setNext(new Level2Support())
          .setNext(new Level3Support())
          .setNext(new ExecutiveSupport());

        SupportTicket[] tickets = {
            new SupportTicket("Password reset request",       Severity.LOW),
            new SupportTicket("Account billing discrepancy",  Severity.MEDIUM),
            new SupportTicket("Data loss on production DB",   Severity.HIGH),
            new SupportTicket("Full system outage",           Severity.CRITICAL),
        };

        for (SupportTicket ticket : tickets) {
            System.out.println("--- Incoming: " + ticket);
            l1.handle(ticket);
            System.out.println();
        }
    }
}
