"""
Command Pattern

Intent: Encapsulate a request as an object, letting you parameterise clients,
queue/log requests, and support undoable operations.

Python approach: commands are callable objects (or plain functions for simple cases).
The history stack enables undo.

Example: smart home controller with light and thermostat commands.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque


# ── Command interface ─────────────────────────────────────────────────────────

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


# ── Receivers ─────────────────────────────────────────────────────────────────

class Light:
    def __init__(self, location: str) -> None:
        self.location = location
        self.is_on    = False
        self.brightness = 100  # 0-100 %

    def turn_on(self)             -> None: self.is_on = True;  print(f"  💡 {self.location} light ON")
    def turn_off(self)            -> None: self.is_on = False; print(f"  💡 {self.location} light OFF")
    def set_brightness(self, pct: int) -> None:
        self.brightness = pct
        print(f"  💡 {self.location} brightness → {pct}%")


class Thermostat:
    def __init__(self) -> None:
        self.temperature = 20.0  # °C

    def set_temperature(self, temp: float) -> None:
        self.temperature = temp
        print(f"  🌡  Thermostat → {temp}°C")


# ── Concrete Commands ─────────────────────────────────────────────────────────

class LightOnCommand(Command):
    def __init__(self, light: Light) -> None: self._light = light
    def execute(self) -> None: self._light.turn_on()
    def undo(self)    -> None: self._light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light) -> None: self._light = light
    def execute(self) -> None: self._light.turn_off()
    def undo(self)    -> None: self._light.turn_on()


class DimLightCommand(Command):
    """Saves the previous brightness so undo can restore it exactly."""

    def __init__(self, light: Light, level: int) -> None:
        self._light    = light
        self._level    = level
        self._prev     = light.brightness  # snapshot for undo

    def execute(self) -> None:
        self._prev = self._light.brightness     # capture before changing
        self._light.set_brightness(self._level)

    def undo(self) -> None:
        self._light.set_brightness(self._prev)  # restore exact previous value


class SetTemperatureCommand(Command):
    def __init__(self, thermostat: Thermostat, temp: float) -> None:
        self._thermostat = thermostat
        self._temp       = temp
        self._prev       = thermostat.temperature

    def execute(self) -> None:
        self._prev = self._thermostat.temperature
        self._thermostat.set_temperature(self._temp)

    def undo(self) -> None:
        self._thermostat.set_temperature(self._prev)


class MacroCommand(Command):
    """Composite command: executes a sequence of commands as one unit."""

    def __init__(self, commands: list[Command], name: str = "macro") -> None:
        self._commands = commands
        self._name     = name

    def execute(self) -> None:
        print(f"  [Macro:{self._name}] start")
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        print(f"  [Macro:{self._name}] undo")
        for cmd in reversed(self._commands):   # undo in reverse order
            cmd.undo()


# ── Invoker ───────────────────────────────────────────────────────────────────

class RemoteControl:
    """
    Executes commands and keeps a history stack for undo.
    Knows nothing about lights, thermostats, or any specific device.
    """

    def __init__(self) -> None:
        self._history: deque[Command] = deque()

    def press(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if not self._history:
            print("  Nothing to undo.")
            return
        self._history.pop().undo()


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    living_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    thermostat    = Thermostat()
    remote        = RemoteControl()

    print("=== Issuing commands ===")
    remote.press(LightOnCommand(living_light))
    remote.press(DimLightCommand(living_light, 40))
    remote.press(SetTemperatureCommand(thermostat, 22.5))

    # Macro: "good night" — turn off all lights, lower thermostat
    good_night = MacroCommand([
        LightOffCommand(living_light),
        LightOffCommand(bedroom_light),
        SetTemperatureCommand(thermostat, 17.0),
    ], name="good_night")
    remote.press(good_night)

    print("\n=== Undo last 2 actions ===")
    remote.undo_last()   # undo macro
    remote.undo_last()   # undo thermostat set
