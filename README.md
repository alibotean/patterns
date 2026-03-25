# Gang of Four Design Patterns

Runnable examples of all 23 GoF patterns in **Java** and **Python**.
Each example is self-contained, kept minimal, and uses inline documentation to explain the *why*, not just the *what*.

## Structure

```
docs/       — reference material (pattern list, cheat sheets)
java/       — Java examples  (one subfolder per pattern, single Main.java)
python/     — Python examples (one subfolder per pattern, single main.py)
```

Each language folder mirrors the same three-category layout:

```
creational/   abstract_factory  builder  factory_method  prototype  singleton
structural/   adapter  bridge  composite  decorator  facade  flyweight  proxy
behavioral/   chain_of_responsibility  command  interpreter  iterator  mediator
              memento  observer  state  strategy  template_method  visitor
```

## Running an example

**Java** — compile and run from the repo root:
```bash
javac java/creational/singleton/Main.java
java  -cp java creational.singleton.Main
```

**Python** — run directly:
```bash
python python/creational/singleton/main.py
```

## Pattern reference

### Creational — *how objects are created*

| Pattern | One-liner | Java scenario | Python scenario |
|---|---|---|---|
| Abstract Factory | Families of related objects | OS-aware UI widgets (Button + Checkbox) | UI theme families (Button + Tooltip) |
| Builder | Step-by-step construction | Fluent `HttpRequest.Builder` | Fluent `PizzaBuilder` → frozen dataclass |
| Factory Method | Subclass decides what to instantiate | Notification services (Email/SMS/Push) | Report exporters (CSV/JSON/Markdown) |
| Prototype | Clone instead of constructing | Shape registry (Circle, Rectangle) | Game enemy cloning via `copy.deepcopy` |
| Singleton | One instance, global access | Thread-safe `AppLogger` | `Configuration` store via `__new__` |

### Structural — *how objects are composed*

| Pattern | One-liner | Java scenario | Python scenario |
|---|---|---|---|
| Adapter | Make incompatible interfaces compatible | XML sender wrapping a JSON analytics lib | Legacy CSV parser → dict `DataReader` |
| Bridge | Decouple abstraction from implementation | Shapes × Renderers (Vector/Raster) | Message types × delivery channels |
| Composite | Tree of uniform part/whole objects | File system (File + Folder) | Restaurant menu (MenuItem + Menu) |
| Decorator | Attach responsibilities without subclassing | Stackable coffee add-ons | OOP text renderer + `@retry`/`@logged` |
| Facade | Simplified interface to a subsystem | Home theater (`watchMovie()`) | Video conversion pipeline |
| Flyweight | Share fine-grained objects efficiently | Forest of trees (3 shared TreeTypes) | Text editor character styles (`__slots__`) |
| Proxy | Controlled access to another object | Virtual image proxy (lazy load) | Lazy + protection + logging DB proxies |

### Behavioral — *how objects communicate*

| Pattern | One-liner | Java scenario | Python scenario |
|---|---|---|---|
| Chain of Responsibility | Pass request along a handler chain | Support ticket escalation (L1→L2→L3) | HTTP middleware (auth → rate-limit → log) |
| Command | Encapsulate a request as an object | Text editor with undo stack | Smart home remote with `MacroCommand` |
| Interpreter | Evaluate sentences in a grammar | Arithmetic expression AST | Boolean rule engine (`age >= 18 AND …`) |
| Iterator | Sequential access without exposing internals | Typed `BoundedStack` iterator | BST with in-order/pre-order/BFS via generators |
| Mediator | Central hub for object interaction | Chat room (users never reference each other) | Air traffic control tower |
| Memento | Capture and restore internal state | Text editor undo (opaque snapshots) | Drawing canvas with undo/redo |
| Observer | Notify dependents on state change | Stock market price alerts | Weather station with callable listeners |
| State | Behaviour changes with internal state | Traffic light (Red→Green→Yellow) | Order lifecycle (Pending→Shipped→Delivered) |
| Strategy | Interchangeable algorithms | Pluggable sort algorithms | Payment methods + callable sort keys |
| Template Method | Fixed skeleton, variable steps | Sales/HR report generation | CSV/JSON ETL pipeline |
| Visitor | New operations without changing elements | Shape area + description visitors | DOM HTML renderer + `@singledispatch` |

## Design principles behind the examples

- **Composition over inheritance** — preferred wherever the pattern allows.
- **Program to interfaces** — Java uses `interface`/`abstract class`; Python uses `abc.ABC` or duck-typing where idiomatic.
- **Single Responsibility** — each class has one reason to change.
- Language-specific idioms are used rather than directly translating between the two (e.g., Python's `@singledispatch` for Visitor, `@functools.wraps` for Decorator, generators for Iterator).
