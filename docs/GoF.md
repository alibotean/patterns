**The complete, official list of all 23 Gang of Four (GoF) design patterns** from the classic 1994 book *Design Patterns: Elements of Reusable Object-Oriented Software* by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides.

They are grouped into the three standard categories (Creational, Structural, and Behavioral) exactly as presented in the original book, with a one-line purpose for each.

### Creational Patterns (5) – Deal with object creation
1. **Abstract Factory** – Provides an interface for creating families of related or dependent objects without specifying their concrete classes.
1. **Builder** – Separates the construction of a complex object from its representation so the same process can create different representations.
1. **Factory Method** – Defines an interface for creating an object, but lets subclasses decide which class to instantiate.
1. **Prototype** – Specifies the kinds of objects to create using a prototypical instance and creates new objects by copying this prototype.
1. **Singleton** – Ensures a class has only one instance and provides a global point of access to it.

### Structural Patterns (7) – Deal with object composition and class/inheritance structures
1. **Adapter** – Converts the interface of a class into another interface clients expect (also known as Wrapper).
1. **Bridge** – Decouples an abstraction from its implementation so the two can vary independently.
1. **Composite** – Composes objects into tree structures to represent part-whole hierarchies; lets clients treat individual objects and compositions uniformly.
1. **Decorator** – Attaches additional responsibilities to an object dynamically; provides a flexible alternative to subclassing for extending functionality.
1. **Facade** – Provides a unified interface to a set of interfaces in a subsystem; defines a higher-level interface that makes the subsystem easier to use.
1. **Flyweight** – Uses sharing to support large numbers of fine-grained objects efficiently.
1. **Proxy** – Provides a surrogate or placeholder for another object to control access to it.

### Behavioral Patterns (11) – Deal with algorithms, responsibilities, and communication between objects
1. **Chain of Responsibility** – Avoids coupling the sender of a request to its receiver by giving more than one object a chance to handle the request; chains the receiving objects and passes the request along the chain until an object handles it.
1. **Command** – Encapsulates a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.
1. **Interpreter** – Given a language, defines a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.
1. **Iterator** – Provides a way to access the elements of an aggregate object sequentially without exposing its underlying representation.
1. **Mediator** – Defines an object that encapsulates how a set of objects interact; promotes loose coupling by keeping objects from referring to each other explicitly and allows their interaction to be varied independently.
1. **Memento** – Without violating encapsulation, captures and externalizes an object’s internal state so that the object can be restored to this state later.
1. **Observer** – Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically (also known as Publish-Subscribe).
1. **State** – Allows an object to alter its behavior when its internal state changes; the object will appear to change its class.
1. **Strategy** – Defines a family of algorithms, encapsulates each one, and makes them interchangeable; lets the algorithm vary independently from clients that use it.
1. **Template Method** – Defines the skeleton of an algorithm in an operation, deferring some steps to subclasses; lets subclasses redefine certain steps of an algorithm without changing the algorithm’s structure.
1. **Visitor** – Represents an operation to be performed on the elements of an object structure; lets you define a new operation without changing the classes of the elements on which it operates.

These 23 patterns are the foundational catalog that almost every modern design-pattern discussion references.
