
"""Thread-safe controller for manual monitoring cycles."""

from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Any


class MonitoringController:
    """Runs monitoring cycles in the background and exposes their status."""

    def __init__(
        self,
        monitoring_manager: Any,
        execution_lock: Lock,
    ) -> None:
        self._monitoring_manager = monitoring_manager
        self._execution_lock = execution_lock
        self._executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="monitoring",
        )
        self._lock = Lock()
        self._status = {
            "state": "idle",
            "message": "No monitoring cycle has been started.",
        }
        self._future: Future | None = None

    def get_status(self) -> dict[str, str]:
        """Return a snapshot of the current monitoring status."""
        with self._lock:
            return self._status.copy()

    def start_cycle(self) -> tuple[bool, dict[str, str]]:
        """Schedule a monitoring cycle unless one is already running."""
        with self._lock:
            if self._status["state"] == "running":
                return False, self._status.copy()

            if not self._execution_lock.acquire(blocking=False):
                return False, {
                    "state": "busy",
                    "message": "Another monitoring cycle is already running.",
                }

            self._status = {
                "state": "running",
                "message": "Monitoring cycle is running.",
            }

            try:
                self._future = self._executor.submit(self._run_cycle)
            except RuntimeError:
                self._execution_lock.release()
                self._status = {
                    "state": "failed",
                    "message": "Could not start the monitoring worker.",
                }
                return False, self._status.copy()

            return True, self._status.copy()

    def _run_cycle(self) -> None:
        """Execute the existing pipeline and record its outcome."""
        try:
            outcome = self._monitoring_manager.run_cycle()

        except Exception:
            with self._lock:
                self._status = {
                    "state": "failed",
                    "message": (
                        "Monitoring cycle failed. Check application logs."
                    ),
                }

        else:
            with self._lock:
                if outcome is False:
                    self._status = {
                        "state": "aborted",
                        "message": (
                            "Monitoring cycle stopped because "
                            "validation failed."
                        ),
                    }
                else:
                    self._status = {
                        "state": "completed",
                        "message": "Monitoring cycle finished.",
                    }

        finally:
            self._execution_lock.release()

    def shutdown(self) -> None:
        """Wait for monitoring work to finish before shutting down."""
        self._executor.shutdown(wait=True)
