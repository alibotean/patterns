package behavioral.state;

/**
 * State Pattern
 *
 * Intent: Allow an object to alter its behaviour when its internal state changes.
 * The object will appear to change its class.
 *
 * Without State: a single class with large if/switch blocks that check current state.
 * With State:    each state is its own class; transitions are explicit method calls.
 *
 * Classic example: a traffic light that cycles Red → Green → Yellow → Red.
 */

// ── State interface ───────────────────────────────────────────────────────────

/**
 * Declares behaviour that varies by state.
 * Each concrete state implements these methods for its own situation.
 */
interface TrafficLightState {
    void display();        // what the light currently shows
    void next(TrafficLight light); // advance to the next state
}

// ── Context ───────────────────────────────────────────────────────────────────

/**
 * The context holds a reference to the current state and delegates to it.
 * Client code only calls context methods — it never talks to state objects directly.
 */
class TrafficLight {
    private TrafficLightState currentState;

    /** Starts in red. */
    TrafficLight() {
        currentState = new RedState();
    }

    /** Called by concrete states during a transition. */
    public void setState(TrafficLightState state) {
        this.currentState = state;
    }

    /** Delegate to the current state. */
    public void display() { currentState.display(); }

    /** Trigger a state transition. */
    public void advance() { currentState.next(this); }
}

// ── Concrete States ───────────────────────────────────────────────────────────

class RedState implements TrafficLightState {
    @Override
    public void display() { System.out.println("🔴 RED    — Stop"); }

    @Override
    public void next(TrafficLight light) {
        System.out.println("  (Red → Green)");
        light.setState(new GreenState());
    }
}

class GreenState implements TrafficLightState {
    @Override
    public void display() { System.out.println("🟢 GREEN  — Go"); }

    @Override
    public void next(TrafficLight light) {
        System.out.println("  (Green → Yellow)");
        light.setState(new YellowState());
    }
}

class YellowState implements TrafficLightState {
    @Override
    public void display() { System.out.println("🟡 YELLOW — Slow down"); }

    @Override
    public void next(TrafficLight light) {
        System.out.println("  (Yellow → Red)");
        light.setState(new RedState());
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        TrafficLight light = new TrafficLight();

        // Cycle through 6 ticks — the context's behaviour changes with each state
        for (int i = 0; i < 6; i++) {
            light.display();
            light.advance();
        }
    }
}
