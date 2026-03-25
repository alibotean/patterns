"""
Observer Pattern  (Publish-Subscribe)

Intent: Define a one-to-many dependency so that when one object changes state,
all dependents are notified and updated automatically.

Python approach: a minimal event bus using a dict of listener lists.
Using a generic EventBus makes it reusable across any domain — no Observer
interface inheritance is required thanks to duck-typing (any callable works).

Example: a weather station that notifies multiple displays and loggers.
"""

from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable


# ── Event types ────────────────────────────────────────────────────────────────

@dataclass
class WeatherReading:
    temperature: float   # °C
    humidity:    float   # %
    pressure:    float   # hPa


# ── Subject (Observable) ───────────────────────────────────────────────────────

# Type alias: a listener is any callable that accepts the event payload
Listener = Callable[[WeatherReading], None]


class WeatherStation:
    """
    Publishes WeatherReading events to registered listeners.
    Listeners can be methods, lambdas, or any callable — no base class required.
    """

    def __init__(self, name: str) -> None:
        self._name      = name
        self._listeners: list[Listener] = []

    def subscribe(self, listener: Listener) -> None:
        self._listeners.append(listener)

    def unsubscribe(self, listener: Listener) -> None:
        self._listeners.remove(listener)

    def set_measurement(self, temp: float, humidity: float, pressure: float) -> None:
        reading = WeatherReading(temp, humidity, pressure)
        print(f"\n[{self._name}] New reading: "
              f"{temp}°C  {humidity}% RH  {pressure} hPa")
        self._notify(reading)

    def _notify(self, reading: WeatherReading) -> None:
        for listener in self._listeners:
            listener(reading)


# ── Concrete Observers ─────────────────────────────────────────────────────────

class CurrentConditionsDisplay:
    """Always shows the latest reading."""

    def __call__(self, reading: WeatherReading) -> None:
        print(f"  [CurrentConditions] Temp: {reading.temperature}°C  "
              f"Humidity: {reading.humidity}%")


class StatisticsDisplay:
    """Tracks min, max, and average temperature across all readings."""

    def __init__(self) -> None:
        self._readings: list[float] = []

    def __call__(self, reading: WeatherReading) -> None:
        self._readings.append(reading.temperature)
        mn = min(self._readings)
        mx = max(self._readings)
        av = sum(self._readings) / len(self._readings)
        print(f"  [Statistics]       Temp min/avg/max: {mn:.1f}/{av:.1f}/{mx:.1f}°C")


class AlertSystem:
    """Fires an alert when temperature or humidity crosses a threshold."""

    def __init__(self, max_temp: float, max_humidity: float) -> None:
        self._max_temp     = max_temp
        self._max_humidity = max_humidity

    def __call__(self, reading: WeatherReading) -> None:
        if reading.temperature > self._max_temp:
            print(f"  [ALERT] ⚠️  High temperature: {reading.temperature}°C "
                  f"(threshold: {self._max_temp}°C)")
        if reading.humidity > self._max_humidity:
            print(f"  [ALERT] ⚠️  High humidity: {reading.humidity}% "
                  f"(threshold: {self._max_humidity}%)")


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    station = WeatherStation("Roof Sensor")

    current = CurrentConditionsDisplay()
    stats   = StatisticsDisplay()
    alerts  = AlertSystem(max_temp=35.0, max_humidity=90.0)

    station.subscribe(current)
    station.subscribe(stats)
    station.subscribe(alerts)

    station.set_measurement(22.5, 65.0, 1013.2)
    station.set_measurement(28.0, 72.0, 1010.5)
    station.set_measurement(37.1, 91.5, 1008.0)  # triggers both alerts

    # Unsubscribe the alert system — subsequent readings won't trigger it
    print("\n[Unsubscribing AlertSystem]")
    station.unsubscribe(alerts)
    station.set_measurement(38.0, 95.0, 1005.0)  # no alert fired
