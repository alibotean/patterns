package creational.factory_method;

/**
 * Factory Method Pattern
 *
 * Intent: Define an interface for creating an object, but let subclasses decide
 * which class to instantiate. Defers instantiation to subclasses.
 *
 * Use when: The exact type of object to create isn't known until runtime,
 * or when subclasses should control what gets created.
 */

// ── Product interface ────────────────────────────────────────────────────────

/** All notifications share this interface. */
interface Notification {
    void send(String message);
}

// ── Concrete Products ────────────────────────────────────────────────────────

class EmailNotification implements Notification {
    private final String email;

    EmailNotification(String email) { this.email = email; }

    @Override
    public void send(String message) {
        System.out.printf("Email → %s: \"%s\"%n", email, message);
    }
}

class SmsNotification implements Notification {
    private final String phoneNumber;

    SmsNotification(String phoneNumber) { this.phoneNumber = phoneNumber; }

    @Override
    public void send(String message) {
        System.out.printf("SMS → %s: \"%s\"%n", phoneNumber, message);
    }
}

class PushNotification implements Notification {
    private final String deviceToken;

    PushNotification(String deviceToken) { this.deviceToken = deviceToken; }

    @Override
    public void send(String message) {
        System.out.printf("Push → device[%s]: \"%s\"%n", deviceToken, message);
    }
}

// ── Creator (abstract) ───────────────────────────────────────────────────────

/**
 * The Creator declares the factory method that subclasses must implement.
 * It also contains business logic that relies on Notification objects —
 * the concrete type is irrelevant here, which is the whole point.
 */
abstract class NotificationService {

    /**
     * Factory method — subclasses override this to return a specific product.
     */
    protected abstract Notification createNotification();

    /**
     * Uses the product without knowing its concrete type.
     */
    public void notify(String message) {
        Notification notification = createNotification();
        notification.send(message);
    }
}

// ── Concrete Creators ────────────────────────────────────────────────────────

class EmailService extends NotificationService {
    private final String email;

    EmailService(String email) { this.email = email; }

    @Override
    protected Notification createNotification() {
        return new EmailNotification(email);
    }
}

class SmsService extends NotificationService {
    private final String phone;

    SmsService(String phone) { this.phone = phone; }

    @Override
    protected Notification createNotification() {
        return new SmsNotification(phone);
    }
}

class PushService extends NotificationService {
    private final String token;

    PushService(String token) { this.token = token; }

    @Override
    protected Notification createNotification() {
        return new PushNotification(token);
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // The caller works with NotificationService — it never names the concrete product
        NotificationService[] services = {
            new EmailService("alice@example.com"),
            new SmsService("+1-555-0100"),
            new PushService("tok-abc123")
        };

        for (NotificationService service : services) {
            service.notify("Your order has shipped!");
        }
    }
}
