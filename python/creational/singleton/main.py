"""
Singleton Pattern

Intent: Ensure a class has only one instance and provide a global access point to it.

Python approach: override __new__ to control instantiation.
A module-level variable would also work in Python, but the class-based approach
makes the pattern explicit and works across imports.
"""


class Configuration:
    """
    Application-wide configuration store.
    Only one instance ever exists — all callers share the same config dict.
    """

    _instance: "Configuration | None" = None

    def __new__(cls) -> "Configuration":
        # On first call: create and cache the instance.
        # On every subsequent call: return the cached one.
        if cls._instance is None:
            print("[Configuration] Creating the sole instance.")
            cls._instance = super().__new__(cls)
            cls._instance._settings: dict = {}   # initialise only once
        return cls._instance

    def set(self, key: str, value: object) -> None:
        self._settings[key] = value

    def get(self, key: str, default: object = None) -> object:
        return self._settings.get(key, default)

    def __repr__(self) -> str:
        return f"Configuration({self._settings})"


if __name__ == "__main__":
    # Both variables resolve to the exact same object.
    cfg1 = Configuration()
    cfg2 = Configuration()

    cfg1.set("debug", True)
    cfg1.set("db_host", "localhost")

    # Changes made through cfg1 are visible through cfg2 — same instance.
    print(f"debug via cfg2 : {cfg2.get('debug')}")
    print(f"db_host via cfg2: {cfg2.get('db_host')}")

    print(f"\nSame instance? {cfg1 is cfg2}")   # True
    print(cfg1)
