"""Generic test doubles for time and concurrency. No domain logic."""
import sys
import threading

import pytest


class FakeClock:
    """Manually advanced monotonic clock. Inject where code would call time.monotonic()."""

    def __init__(self, now: float = 0.0) -> None:
        self._now = now

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> float:
        self._now += seconds
        return self._now


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


def run_concurrently(fn, threads: int = 8, iterations: int = 1, collide_every_iteration: bool = True):
    """Run fn(i) on N threads that genuinely interleave. Returns results, re-raises failures.

    Threads rendezvous on a barrier before *every* iteration and the GIL switch interval is
    dropped for the duration. Syncing only once at startup is not enough -- threads then run to
    completion one after another and no race ever appears.

    If a test still passes with the lock removed, the critical section is too narrow for a GIL
    switch to land inside it. Widen it (more threads, more iterations) or assert on a shared
    path that does real work. A concurrency test that cannot fail is worthless.
    """
    barrier = threading.Barrier(threads)
    results: list = []
    errors: list[BaseException] = []
    lock = threading.Lock()

    def worker(index: int) -> None:
        try:
            for _ in range(iterations):
                if collide_every_iteration:
                    barrier.wait()
                value = fn(index)
                with lock:
                    results.append(value)
        except BaseException as exc:
            with lock:
                errors.append(exc)
            barrier.abort()  # release peers instead of deadlocking them

    original_interval = sys.getswitchinterval()
    sys.setswitchinterval(1e-6)
    try:
        workers = [threading.Thread(target=worker, args=(i,)) for i in range(threads)]
        for w in workers:
            w.start()
        for w in workers:
            w.join(timeout=10)
    finally:
        sys.setswitchinterval(original_interval)

    if errors:
        # A broken barrier is collateral damage from another thread's failure, not the cause.
        real = [e for e in errors if not isinstance(e, threading.BrokenBarrierError)]
        raise (real or errors)[0]
    return results
