import asyncio
import contextvars
from concurrent.futures import ThreadPoolExecutor, as_completed

from goodlog import ephemeral_info_context
from goodlog.extra_info.store import (
    _ExtraLoggingInfo,
    _ephemeral_info,
    get_info,
)


def _reset_store() -> None:
    _ExtraLoggingInfo._instances.clear()
    _ephemeral_info.set({})


def test_async_concurrency_isolation() -> None:
    """
    Verify that concurrent async tasks each see their own ephemeral info,
    not another task's. This would fail with the old singleton _more_info.
    """
    _reset_store()
    _ExtraLoggingInfo(service="test")
    errors: list[str] = []

    async def worker(task_id: int) -> None:
        with ephemeral_info_context(request_id=str(task_id)):
            await asyncio.sleep(0.05)
            info = get_info()
            actual = info.get("request_id")
            if actual != str(task_id):
                errors.append(
                    f"task {task_id}: expected '{task_id}', got '{actual}'"
                )

    async def run_all() -> None:
        tasks = [asyncio.create_task(worker(i)) for i in range(20)]
        await asyncio.gather(*tasks)

    asyncio.run(run_all())
    assert errors == [], "Context leaked between async tasks:\n" + "\n".join(
        errors
    )


def test_thread_concurrency_isolation() -> None:
    """
    Verify that concurrent threads each see their own ephemeral info.
    Each thread must copy the context so the ContextVar is isolated.
    """
    _reset_store()
    _ExtraLoggingInfo(service="test")
    errors: list[str] = []

    def worker(task_id: int) -> None:
        with ephemeral_info_context(request_id=str(task_id)):
            import time
            time.sleep(0.05)
            info = get_info()
            actual = info.get("request_id")
            if actual != str(task_id):
                errors.append(
                    f"thread {task_id}: expected '{task_id}', got '{actual}'"
                )

    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [
            pool.submit(contextvars.copy_context().run, worker, i)
            for i in range(20)
        ]
        for f in as_completed(futures):
            f.result()

    assert errors == [], "Context leaked between threads:\n" + "\n".join(
        errors
    )
