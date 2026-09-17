"""Coverage for library/threading.py.

Concurrency helpers whose failure modes only show under contention, which is why they
sat at 63% with the interesting half untested.
"""

import threading
import time
from typing import Any
from dependency.library.threading import excluded, handle_exit, threaded


# ── excluded ─────────────────────────────────────────────────────────────────


def test_excluded_runs_the_function_when_uncontended() -> None:
    @excluded()
    def work() -> str:
        return "ran"

    assert work() == "ran"


def test_excluded_returns_the_default_when_the_lock_is_held() -> None:
    """The point of the decorator: a second caller is turned away, not queued.

    blocking=False means an already-running call makes the next one a no-op — the
    behaviour you want for a periodic task that must not overlap itself.
    """
    entered = threading.Event()
    release = threading.Event()
    results: list[Any] = []

    @excluded(default="rejected")
    def work() -> str:
        entered.set()
        release.wait(timeout=2)
        return "ran"

    holder = threading.Thread(target=lambda: results.append(work()))
    holder.start()
    assert entered.wait(timeout=2), "the first call never started"

    assert work() == "rejected"

    release.set()
    holder.join(timeout=2)
    assert results == ["ran"]


def test_excluded_releases_the_lock_after_an_exception() -> None:
    """A lock that is not released on failure turns one error into a dead service."""

    @excluded(default="rejected")
    def work(should_raise: bool) -> str:
        if should_raise:
            raise ValueError("boom")
        return "ran"

    try:
        work(True)
    except ValueError:
        pass

    assert work(False) == "ran"


def test_excluded_blocking_waits_instead_of_rejecting() -> None:
    order: list[str] = []
    started = threading.Event()

    @excluded(blocking=True)
    def work(tag: str) -> None:
        started.set()
        time.sleep(0.05)
        order.append(tag)

    first = threading.Thread(target=work, args=("first",))
    first.start()
    assert started.wait(timeout=2)
    work("second")
    first.join(timeout=2)

    assert order == ["first", "second"], "blocking=True must serialise, not drop"


# ── threaded ─────────────────────────────────────────────────────────────────


def test_threaded_runs_off_the_calling_thread() -> None:
    done = threading.Event()
    where: list[int] = []

    @threaded(name="probe")
    def work() -> None:
        where.append(threading.get_ident())
        done.set()

    work()
    assert done.wait(timeout=2), "the threaded function never ran"
    assert where and where[0] != threading.get_ident()


def test_threaded_returns_none_immediately() -> None:
    """It schedules; it does not hand back a result. Anything needing one wants
    DeferredService.run, not this."""

    @threaded()
    def work() -> str:
        return "never reaches the caller"

    assert work() is None


def test_threaded_passes_arguments_through() -> None:
    done = threading.Event()
    seen: list[tuple[int, str]] = []

    @threaded()
    def work(number: int, label: str = "") -> None:
        seen.append((number, label))
        done.set()

    work(7, label="tagged")
    assert done.wait(timeout=2)
    assert seen == [(7, "tagged")]


# ── handle_exit ──────────────────────────────────────────────────────────────


def test_handle_exit_passes_normal_calls_through() -> None:
    calls: list[str] = []

    @handle_exit
    def work() -> None:
        calls.append("ran")

    work()
    assert calls == ["ran"]


def test_handle_exit_does_not_swallow_other_exceptions() -> None:
    """Only KeyboardInterrupt is special. A bug must still surface."""

    @handle_exit
    def work() -> None:
        raise ValueError("a real failure")

    try:
        work()
    except ValueError:
        return
    raise AssertionError("handle_exit swallowed a genuine exception")
