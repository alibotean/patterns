"""
Mediator Pattern

Intent: Define an object that encapsulates how a set of objects interact.
Promotes loose coupling by keeping objects from referring to each other explicitly.

Example: an air-traffic control (ATC) tower.
Planes never communicate directly; they only talk to the tower, which coordinates
all landings and departures. Adding a new plane doesn't require any existing
plane to change.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Mediator interface ─────────────────────────────────────────────────────────

class AirTrafficControl(ABC):
    @abstractmethod
    def notify(self, sender: "Aircraft", event: str) -> None: ...

    @abstractmethod
    def register(self, aircraft: "Aircraft") -> None: ...


# ── Colleague ──────────────────────────────────────────────────────────────────

class Aircraft:
    """
    Each aircraft holds only a reference to the ATC tower.
    It never addresses other planes directly — all coordination goes through
    the mediator.
    """

    def __init__(self, callsign: str, atc: AirTrafficControl) -> None:
        self._callsign = callsign
        self._atc      = atc
        self._state    = "parked"
        atc.register(self)

    @property
    def callsign(self) -> str: return self._callsign

    @property
    def state(self) -> str: return self._state

    def request_takeoff(self) -> None:
        print(f"  [{self._callsign}] Requesting takeoff clearance")
        self._atc.notify(self, "request_takeoff")

    def request_landing(self) -> None:
        print(f"  [{self._callsign}] Requesting landing clearance")
        self._atc.notify(self, "request_landing")

    # Called by the mediator — the aircraft reacts to tower instructions
    def cleared_for_takeoff(self) -> None:
        self._state = "airborne"
        print(f"  [{self._callsign}] Tower cleared us for takeoff — ROLLING")

    def cleared_to_land(self) -> None:
        self._state = "landed"
        print(f"  [{self._callsign}] Tower cleared us to land — DESCENDING")

    def hold_position(self, reason: str) -> None:
        print(f"  [{self._callsign}] Tower says HOLD: {reason}")


# ── Concrete Mediator ─────────────────────────────────────────────────────────

class ControlTower(AirTrafficControl):
    """
    Coordinates all planes on or near the runway.
    Enforces the rule: at most one plane may use the runway at a time.
    """

    def __init__(self) -> None:
        self._aircraft:     dict[str, Aircraft] = {}
        self._runway_busy:  bool = False

    def register(self, aircraft: Aircraft) -> None:
        self._aircraft[aircraft.callsign] = aircraft
        print(f"[Tower] Registered {aircraft.callsign}")

    def notify(self, sender: Aircraft, event: str) -> None:
        if event == "request_takeoff":
            if self._runway_busy:
                sender.hold_position("runway occupied")
            else:
                self._runway_busy = True
                sender.cleared_for_takeoff()

        elif event == "request_landing":
            if self._runway_busy:
                sender.hold_position("runway occupied — enter holding pattern")
            else:
                self._runway_busy = True
                sender.cleared_to_land()

        elif event in ("airborne", "landed"):
            # Plane has vacated the runway
            self._runway_busy = False
            print(f"[Tower] Runway is now free (vacated by {sender.callsign})")


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tower = ControlTower()

    print("\n=== Registering aircraft ===")
    aa101 = Aircraft("AA101", tower)
    ba202 = Aircraft("BA202", tower)
    ua303 = Aircraft("UA303", tower)

    print("\n=== AA101 takes off ===")
    aa101.request_takeoff()
    tower.notify(aa101, "airborne")     # AA101 has left the runway

    print("\n=== BA202 and UA303 both want to land ===")
    ba202.request_landing()             # gets clearance
    ua303.request_landing()             # held — runway busy

    tower.notify(ba202, "landed")       # BA202 vacated
    print("\n=== UA303 tries again ===")
    ua303.request_landing()             # now cleared
