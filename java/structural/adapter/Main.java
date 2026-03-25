package structural.adapter;

/**
 * Adapter Pattern
 *
 * Intent: Convert the interface of a class into another interface that clients expect.
 * Lets otherwise-incompatible classes work together.
 *
 * Use when: You want to reuse an existing class but its interface doesn't match what
 * the rest of your system expects (e.g., integrating a third-party library).
 */

// ── Target interface — what the client expects ───────────────────────────────

/**
 * The interface our application code uses to send data.
 * Expects XML strings.
 */
interface XmlDataSender {
    void send(String xmlData);
}

// ── Adaptee — the existing class with an incompatible interface ──────────────

/**
 * A third-party analytics library that only understands JSON.
 * We cannot (or don't want to) modify this class.
 */
class ThirdPartyAnalytics {
    public void trackEvent(String jsonData) {
        System.out.println("[Analytics] Received JSON: " + jsonData);
    }
}

// ── Adapter ──────────────────────────────────────────────────────────────────

/**
 * The Adapter implements the target interface and wraps the adaptee.
 * It translates XML → JSON so the client never has to know the difference.
 */
class AnalyticsAdapter implements XmlDataSender {

    private final ThirdPartyAnalytics analytics;

    AnalyticsAdapter(ThirdPartyAnalytics analytics) {
        this.analytics = analytics;
    }

    /**
     * Called by the client with XML — converts it to JSON, then delegates
     * to the wrapped ThirdPartyAnalytics instance.
     */
    @Override
    public void send(String xmlData) {
        String json = convertXmlToJson(xmlData);
        analytics.trackEvent(json);
    }

    /** Minimal XML-to-JSON conversion for demonstration purposes. */
    private String convertXmlToJson(String xml) {
        // Real code would use a proper parser; this keeps the example focused.
        return xml.replace("<event>", "{\"event\":\"")
                  .replace("</event>", "\"}");
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // The client knows only XmlDataSender — it has no idea there's JSON involved
        XmlDataSender sender = new AnalyticsAdapter(new ThirdPartyAnalytics());

        sender.send("<event>page_view</event>");
        sender.send("<event>button_click</event>");
    }
}
