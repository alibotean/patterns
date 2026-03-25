package structural.proxy;

/**
 * Proxy Pattern
 *
 * Intent: Provide a surrogate or placeholder for another object to control access to it.
 *
 * Common proxy types:
 *   • Virtual proxy  — delays expensive creation until first use (lazy init)
 *   • Protection proxy — checks permissions before forwarding the call
 *   • Logging proxy  — logs calls before/after forwarding
 *
 * This example shows a Virtual Proxy: the real image (expensive to load) is only
 * instantiated when display() is called for the first time.
 */

// ── Subject interface ────────────────────────────────────────────────────────

/** Both the real image and the proxy implement this. */
interface Image {
    void display();
}

// ── Real Subject ─────────────────────────────────────────────────────────────

/**
 * Loading a high-resolution image from disk is expensive.
 * We don't want to do it unless the image is actually rendered.
 */
class HighResolutionImage implements Image {
    private final String filename;

    HighResolutionImage(String filename) {
        this.filename = filename;
        loadFromDisk(); // expensive — happens immediately in the real object
    }

    private void loadFromDisk() {
        System.out.println("[RealImage] Loading from disk: " + filename);
    }

    @Override
    public void display() {
        System.out.println("[RealImage] Displaying: " + filename);
    }
}

// ── Proxy ────────────────────────────────────────────────────────────────────

/**
 * The proxy has the same interface as HighResolutionImage.
 * It holds a reference (initially null) and creates the real object only on
 * the first call to display() — subsequent calls reuse the cached instance.
 */
class ImageProxy implements Image {
    private final String filename;
    private HighResolutionImage realImage; // null until first display()

    ImageProxy(String filename) {
        // Constructing the proxy is cheap — no disk I/O here
        this.filename  = filename;
        this.realImage = null;
        System.out.println("[Proxy] Created proxy for: " + filename);
    }

    @Override
    public void display() {
        if (realImage == null) {
            // First access — pay the cost of loading now
            realImage = new HighResolutionImage(filename);
        }
        // Subsequent accesses reuse the already-loaded real image
        realImage.display();
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        System.out.println("=== Creating proxies (no images loaded yet) ===");
        Image img1 = new ImageProxy("photo_holiday.jpg");
        Image img2 = new ImageProxy("photo_portrait.jpg");

        System.out.println("\n=== Displaying img1 for the first time (loads now) ===");
        img1.display();

        System.out.println("\n=== Displaying img1 again (no reload) ===");
        img1.display();

        System.out.println("\n=== img2 is never displayed — its real object is never created ===");
        // img2.display(); // uncomment to trigger loading
    }
}
