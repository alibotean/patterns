"""
Chain of Responsibility Pattern

Intent: Avoid coupling the sender of a request to its receiver by giving multiple
objects a chance to handle it. Pass the request along the chain until one handles it.

Python approach: handlers are plain callables or objects; the chain is assembled
by linking each handler to the next via a reference.

Example: HTTP middleware pipeline (authentication → rate limiting → logging → handler).
Each middleware either short-circuits with an error response or forwards the request.
"""

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


# ── Request / Response ────────────────────────────────────────────────────────

@dataclass
class HttpRequest:
    method:  str
    path:    str
    api_key: str | None = None
    user_id: str | None = None   # filled in by auth middleware


@dataclass
class HttpResponse:
    status:  int
    body:    str

    def __str__(self) -> str:
        return f"HTTP {self.status}: {self.body}"


# ── Handler interface ─────────────────────────────────────────────────────────

class Middleware(ABC):
    """Each middleware in the chain either handles the request or forwards it."""

    def __init__(self) -> None:
        self._next: Middleware | None = None

    def set_next(self, handler: Middleware) -> Middleware:
        """Link the next handler; return it so calls can be chained fluently."""
        self._next = handler
        return handler

    def forward(self, request: HttpRequest) -> HttpResponse:
        """Pass request to the next handler, or return 500 if chain is broken."""
        if self._next:
            return self._next.handle(request)
        return HttpResponse(500, "No handler at end of chain")

    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse: ...


# ── Concrete Middleware ───────────────────────────────────────────────────────

# Simulated valid API keys and their owners
_VALID_KEYS: dict[str, str] = {
    "key-alice": "alice",
    "key-bob":   "bob",
}

class AuthMiddleware(Middleware):
    """Validates the API key and attaches user_id to the request."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        if not request.api_key or request.api_key not in _VALID_KEYS:
            print(f"  [Auth] Rejected — invalid key: {request.api_key!r}")
            return HttpResponse(401, "Unauthorized")
        request.user_id = _VALID_KEYS[request.api_key]
        print(f"  [Auth] Authenticated as '{request.user_id}'")
        return self.forward(request)


_REQUEST_COUNTS: dict[str, int] = {}
_RATE_LIMIT = 2  # max requests per user (tiny limit to demo rejection)

class RateLimitMiddleware(Middleware):
    """Rejects requests once a user exceeds the rate limit."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        user = request.user_id or "anonymous"
        _REQUEST_COUNTS[user] = _REQUEST_COUNTS.get(user, 0) + 1
        if _REQUEST_COUNTS[user] > _RATE_LIMIT:
            print(f"  [RateLimit] '{user}' exceeded limit ({_REQUEST_COUNTS[user]})")
            return HttpResponse(429, "Too Many Requests")
        print(f"  [RateLimit] '{user}' request #{_REQUEST_COUNTS[user]} — ok")
        return self.forward(request)


class LoggingMiddleware(Middleware):
    """Logs every request that makes it this far, then forwards it."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        print(f"  [Log] {request.method} {request.path} by {request.user_id}")
        response = self.forward(request)
        print(f"  [Log] Response: {response.status}")
        return response


class RequestHandler(Middleware):
    """Terminal handler — actually processes the business request."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(200, f"Hello, {request.user_id}! Path: {request.path}")


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Build the chain: Auth → RateLimit → Logging → Handler
    auth = AuthMiddleware()
    auth.set_next(RateLimitMiddleware()) \
        .set_next(LoggingMiddleware()) \
        .set_next(RequestHandler())

    requests = [
        HttpRequest("GET",  "/api/hello",   api_key="key-alice"),   # ok
        HttpRequest("GET",  "/api/data",    api_key="key-alice"),   # ok (2nd)
        HttpRequest("GET",  "/api/data",    api_key="key-alice"),   # rate limited
        HttpRequest("POST", "/api/upload",  api_key=None),          # unauthorized
        HttpRequest("GET",  "/api/hello",   api_key="key-bob"),     # ok
    ]

    for req in requests:
        print(f"\n→ {req.method} {req.path}  key={req.api_key!r}")
        print(auth.handle(req))
