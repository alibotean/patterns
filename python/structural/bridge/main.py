"""
Bridge Pattern

Intent: Decouple an abstraction from its implementation so the two can vary independently.

Without Bridge: adding a new message type AND a new channel would require N×M classes.
With Bridge:    message types and channels grow independently — just N + M classes.

The "bridge" is the channel reference held by Message.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# ── Implementor interface ─────────────────────────────────────────────────────

class Channel(ABC):
    """Low-level delivery mechanism. Messages delegate sending to a Channel."""

    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> None: ...


# ── Concrete Implementors ─────────────────────────────────────────────────────

class EmailChannel(Channel):
    def send(self, recipient: str, subject: str, body: str) -> None:
        print(f"[Email → {recipient}]  Subject: {subject}")
        print(f"  Body: {body}")


class SmsChannel(Channel):
    def send(self, recipient: str, subject: str, body: str) -> None:
        # SMS ignores subject and truncates body
        print(f"[SMS → {recipient}]  {body[:80]}")


class SlackChannel(Channel):
    def send(self, recipient: str, subject: str, body: str) -> None:
        print(f"[Slack → #{recipient}]  *{subject}*  {body}")


# ── Abstraction ───────────────────────────────────────────────────────────────

class Message(ABC):
    """
    High-level abstraction. Knows *what* to communicate (the message type);
    delegates *how* to deliver it to the injected Channel (the bridge).
    """

    def __init__(self, channel: Channel) -> None:
        self._channel = channel   # the bridge

    @abstractmethod
    def send(self, recipient: str) -> None: ...


# ── Refined Abstractions ──────────────────────────────────────────────────────

class AlertMessage(Message):
    def __init__(self, channel: Channel, alert_text: str) -> None:
        super().__init__(channel)
        self._alert_text = alert_text

    def send(self, recipient: str) -> None:
        # Message knows *what* — channel knows *how*
        self._channel.send(recipient, "ALERT", f"⚠️  {self._alert_text}")


class WelcomeMessage(Message):
    def __init__(self, channel: Channel, user_name: str) -> None:
        super().__init__(channel)
        self._user_name = user_name

    def send(self, recipient: str) -> None:
        self._channel.send(
            recipient,
            "Welcome aboard!",
            f"Hi {self._user_name}, thanks for joining us. Here's how to get started…",
        )


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    email = EmailChannel()
    sms   = SmsChannel()
    slack = SlackChannel()

    # Same message type, different channels — no subclass explosion
    print("=== Alerts ===")
    AlertMessage(email, "Disk usage above 90%").send("ops@example.com")
    AlertMessage(sms,   "Disk usage above 90%").send("+1-555-0100")
    AlertMessage(slack, "Disk usage above 90%").send("ops-alerts")

    print("\n=== Welcome messages ===")
    WelcomeMessage(email, "Alice").send("alice@example.com")
    WelcomeMessage(slack, "Bob").send("general")
