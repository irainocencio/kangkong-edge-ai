"""Tests for the MonitoringController."""

from threading import Event, Lock

from app.core.monitoring_controller import MonitoringController


class FakeMonitoringManager:
    def run_cycle(self):
        return None


def test_controller_starts_and_completes_cycle():
    controller = MonitoringController(
        FakeMonitoringManager(),
        execution_lock=Lock(),
    )
    try:
        accepted, status = controller.start_cycle()

        assert accepted is True
        assert status["state"] == "running"

        controller._future.result(timeout=2)

        assert controller.get_status()["state"] == "completed"
    finally:
        controller.shutdown()


def test_controller_rejects_duplicate_trigger_while_running():
    started = Event()
    release = Event()

    class BlockingMonitoringManager:
        def run_cycle(self):
            started.set()
            assert release.wait(timeout=2)

    controller = MonitoringController(
        BlockingMonitoringManager(),
        execution_lock=Lock(),
    )
    try:
        accepted, _ = controller.start_cycle()
        assert accepted is True
        assert started.wait(timeout=2)

        accepted_again, status = controller.start_cycle()

        assert accepted_again is False
        assert status["state"] == "running"
    finally:
        release.set()
        controller.shutdown()


def test_controller_reports_cycle_failure():
    class FailingMonitoringManager:
        def run_cycle(self):
            raise RuntimeError("simulated failure")

    controller = MonitoringController(
        FailingMonitoringManager(),
        execution_lock=Lock(),
    )
    try:
        accepted, _ = controller.start_cycle()
        assert accepted is True

        controller._future.result(timeout=2)

        assert controller.get_status()["state"] == "failed"
    finally:
        controller.shutdown()


def test_controller_rejects_cycle_when_shared_lock_is_held():
    execution_lock = Lock()
    execution_lock.acquire()

    controller = MonitoringController(
        FakeMonitoringManager(),
        execution_lock=execution_lock,
    )

    try:
        accepted, status = controller.start_cycle()

        assert accepted is False
        assert status["state"] == "busy"
    finally:
        execution_lock.release()
        controller.shutdown()