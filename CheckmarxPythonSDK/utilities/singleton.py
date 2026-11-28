"""Process-wide lazy singletons for the API classes.

The module-level convenience functions in e.g. projectsAPI and repoManagerAPI
are backed by these, so repeated calls reuse one API client (connection pool,
cached access token) instead of paying a new client and token fetch per call.
"""
import threading
from typing import Callable, Optional, TypeVar

T = TypeVar("T")


class LazySingleton:
    """Thread-safe lazy singleton; the factory runs once, on first get()."""

    def __init__(self, factory: Callable[[], T]):
        self._factory = factory
        self._instance: Optional[T] = None
        self._lock = threading.Lock()

    def get(self) -> T:
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._factory()
        return self._instance

    def reset(self) -> None:
        """Drop the cached instance (mainly for tests)."""
        with self._lock:
            self._instance = None
