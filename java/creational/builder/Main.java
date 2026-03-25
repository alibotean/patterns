package creational.builder;

/**
 * Builder Pattern
 *
 * Intent: Separate the construction of a complex object from its representation so
 * the same construction process can create different representations.
 *
 * Use when: An object requires many optional parameters or a multi-step setup,
 * and telescoping constructors would become unwieldy.
 */

// ── Product ──────────────────────────────────────────────────────────────────

/**
 * A HTTP request is the product being built.
 * It has required fields (method, url) and many optional ones.
 * Made immutable — all fields are set once by the Builder.
 */
class HttpRequest {
    private final String method;      // required
    private final String url;         // required
    private final String body;        // optional
    private final String contentType; // optional
    private final int    timeoutMs;   // optional
    private final boolean followRedirects; // optional

    // Private constructor — only the inner Builder can call this
    private HttpRequest(Builder builder) {
        this.method           = builder.method;
        this.url              = builder.url;
        this.body             = builder.body;
        this.contentType      = builder.contentType;
        this.timeoutMs        = builder.timeoutMs;
        this.followRedirects  = builder.followRedirects;
    }

    @Override
    public String toString() {
        return String.format(
            "HttpRequest{method='%s', url='%s', body='%s', contentType='%s', timeoutMs=%d, followRedirects=%b}",
            method, url, body, contentType, timeoutMs, followRedirects
        );
    }

    // ── Inner Builder ────────────────────────────────────────────────────────

    /**
     * Fluent builder for HttpRequest.
     * Required parameters go in the constructor; optional ones have setter-like methods.
     * Call build() to get the finished, immutable HttpRequest.
     */
    static class Builder {
        // Required
        private final String method;
        private final String url;

        // Optional — sensible defaults
        private String  body             = null;
        private String  contentType      = "application/json";
        private int     timeoutMs        = 5000;
        private boolean followRedirects  = true;

        /** Start building: provide the two required fields up front. */
        Builder(String method, String url) {
            this.method = method;
            this.url    = url;
        }

        public Builder body(String body)                     { this.body = body; return this; }
        public Builder contentType(String contentType)       { this.contentType = contentType; return this; }
        public Builder timeoutMs(int timeoutMs)              { this.timeoutMs = timeoutMs; return this; }
        public Builder followRedirects(boolean follow)       { this.followRedirects = follow; return this; }

        /** Validate and create the immutable product. */
        public HttpRequest build() {
            if (method == null || method.isBlank()) throw new IllegalStateException("method is required");
            if (url    == null || url.isBlank())    throw new IllegalStateException("url is required");
            return new HttpRequest(this);
        }
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Simple GET — only required fields, defaults for everything else
        HttpRequest get = new HttpRequest.Builder("GET", "https://api.example.com/users")
                .build();

        // Full POST — many optional fields configured via fluent calls
        HttpRequest post = new HttpRequest.Builder("POST", "https://api.example.com/users")
                .body("{\"name\":\"Alice\"}")
                .contentType("application/json")
                .timeoutMs(10_000)
                .followRedirects(false)
                .build();

        System.out.println(get);
        System.out.println(post);
    }
}
