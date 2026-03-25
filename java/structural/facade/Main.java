package structural.facade;

/**
 * Facade Pattern
 *
 * Intent: Provide a unified, simplified interface to a set of interfaces in a subsystem.
 * Makes the subsystem easier to use without hiding it (clients can still bypass the facade).
 *
 * Use when: A subsystem has many components that must be coordinated in a specific order,
 * and you want to shield clients from that complexity.
 */

// ── Subsystem classes (complex internals) ────────────────────────────────────

/** Controls the projector. */
class Projector {
    public void on()        { System.out.println("  Projector: on"); }
    public void off()       { System.out.println("  Projector: off"); }
    public void wideScreen(){ System.out.println("  Projector: wide-screen mode"); }
}

/** Controls the surround-sound amplifier. */
class Amplifier {
    public void on()              { System.out.println("  Amplifier: on"); }
    public void off()             { System.out.println("  Amplifier: off"); }
    public void setVolume(int v)  { System.out.println("  Amplifier: volume → " + v); }
    public void setSurroundSound(){ System.out.println("  Amplifier: surround-sound on"); }
}

/** Controls room lighting. */
class Lights {
    public void dim(int level) { System.out.println("  Lights: dimmed to " + level + "%"); }
    public void on()           { System.out.println("  Lights: full brightness"); }
}

/** Controls the streaming player. */
class StreamingPlayer {
    public void on()           { System.out.println("  StreamingPlayer: on"); }
    public void off()          { System.out.println("  StreamingPlayer: off"); }
    public void play(String m) { System.out.println("  StreamingPlayer: playing \"" + m + "\""); }
    public void stop()         { System.out.println("  StreamingPlayer: stopped"); }
}

// ── Facade ───────────────────────────────────────────────────────────────────

/**
 * HomeTheaterFacade orchestrates all subsystem components behind two simple methods.
 * Clients call watchMovie() / endMovie() — they never touch the subsystem directly.
 */
class HomeTheaterFacade {
    private final Projector      projector;
    private final Amplifier      amplifier;
    private final Lights         lights;
    private final StreamingPlayer player;

    HomeTheaterFacade(Projector projector, Amplifier amplifier,
                      Lights lights, StreamingPlayer player) {
        this.projector = projector;
        this.amplifier = amplifier;
        this.lights    = lights;
        this.player    = player;
    }

    /**
     * One call to set up the entire home theater for movie night.
     * Without the facade the client would have to call ~8 methods in the right order.
     */
    public void watchMovie(String movie) {
        System.out.println("Get ready to watch a movie...");
        lights.dim(10);
        projector.on();
        projector.wideScreen();
        amplifier.on();
        amplifier.setSurroundSound();
        amplifier.setVolume(7);
        player.on();
        player.play(movie);
    }

    /** One call to shut everything down cleanly. */
    public void endMovie() {
        System.out.println("Shutting down the home theater...");
        player.stop();
        player.off();
        amplifier.off();
        projector.off();
        lights.on();
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Wire up the subsystem (could also use dependency injection)
        HomeTheaterFacade theater = new HomeTheaterFacade(
            new Projector(),
            new Amplifier(),
            new Lights(),
            new StreamingPlayer()
        );

        // Client calls are trivially simple — complexity is hidden behind the facade
        theater.watchMovie("Inception");
        System.out.println();
        theater.endMovie();
    }
}
