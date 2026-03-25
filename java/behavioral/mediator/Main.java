package behavioral.mediator;

import java.util.ArrayList;
import java.util.List;

/**
 * Mediator Pattern
 *
 * Intent: Define an object that encapsulates how a set of objects interact.
 * Promotes loose coupling by keeping objects from referring to each other
 * explicitly, and lets you vary their interaction independently.
 *
 * Without Mediator: N participants → up to N² direct references.
 * With Mediator:    N participants → N references to the mediator only.
 *
 * Classic example: a chat room where users never hold references to each other.
 */

// ── Mediator interface ────────────────────────────────────────────────────────

/** The mediator is the hub through which all communication flows. */
interface ChatMediator {
    void sendMessage(String message, User sender);
    void addUser(User user);
}

// ── Colleague ────────────────────────────────────────────────────────────────

/**
 * Each user only knows about the mediator — never about other users.
 * Sending and receiving are both routed through the chat room.
 */
class User {
    private final String       name;
    private final ChatMediator mediator;

    User(String name, ChatMediator mediator) {
        this.name     = name;
        this.mediator = mediator;
    }

    public String getName() { return name; }

    /** Sends a message via the mediator — doesn't know who will receive it. */
    public void send(String message) {
        System.out.printf("[%s → room]: %s%n", name, message);
        mediator.sendMessage(message, this);
    }

    /** Called by the mediator when a message is broadcast to this user. */
    public void receive(String message, User from) {
        System.out.printf("  [%s received from %s]: %s%n", name, from.getName(), message);
    }
}

// ── Concrete Mediator ─────────────────────────────────────────────────────────

/**
 * The ChatRoom acts as the mediator.
 * It knows about all users and decides how to route messages (here: broadcast).
 * Changing routing logic (private messages, groups) only requires changing this class.
 */
class ChatRoom implements ChatMediator {
    private final List<User> users = new ArrayList<>();

    @Override
    public void addUser(User user) { users.add(user); }

    @Override
    public void sendMessage(String message, User sender) {
        // Broadcast to everyone except the sender
        for (User user : users) {
            if (user != sender) {
                user.receive(message, sender);
            }
        }
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        ChatMediator room = new ChatRoom();

        User alice = new User("Alice", room);
        User bob   = new User("Bob",   room);
        User carol = new User("Carol", room);

        room.addUser(alice);
        room.addUser(bob);
        room.addUser(carol);

        // Users send through the mediator — they never reference each other directly
        alice.send("Hello everyone!");
        System.out.println();
        bob.send("Hi Alice!");
    }
}
