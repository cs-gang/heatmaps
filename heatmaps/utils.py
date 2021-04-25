"""Utility functions and classes."""
import asyncio
from typing import Any, Callable

from loguru import logger
from jinja2 import Environment


async def render_page(environment: Environment, *, file: str, **context: Any) -> str:
    """Helper function to render the template.
    Use to give final output in the route functions."""
    template = environment.get_template(file)
    return await template.render_async(**context)


class Loop:
    """Helper class used for background task loops."""

    def __init__(
        self,
        func: Callable,
        *,
        loop: asyncio.AbstractEventLoop,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
    ) -> None:
        self._func = func
        self.loop = loop
        self.interval = seconds
        self.interval += minutes * 60
        self.interval += hours * 3600

        if self.interval == 0:
            raise ValueError("Task loop duration should not be zero.")

        self._exc_count = (
            0
        )  # count exceptions as they occur; if more than 5 in a row; break the loop

    async def _loop(self) -> None:
        while True:
            try:
                await self._func()
            except Exception as e:
                logger.error(f"<TASK LOOP> Exception: {e}")
                # wait before trying again
                await asyncio.sleep(self.interval)

                if self._exc_count > 5:
                    logger.warning(
                        f"<TASK LOOP> Broke the loop {self._func.__name__} as it errored the last 5 runs"
                    )
                    break
                self._exc_count += 1
            else:
                self._exc_count = 0
                await asyncio.sleep(self.interval)

    def start(self) -> asyncio.Task:
        """
        Starts the underlying loop.
        """
        logger.info(f"<TASK LOOP> Starting Task {self._func.__name__}")
        return self.loop.create_task(self._loop())


def loop(
    *,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    event_loop: asyncio.AbstractEventLoop = None,
) -> Callable:
    """
    Decorator to register a coroutine as a loop.
    """

    def decorator(func: Callable) -> Loop:
        nonlocal event_loop
        if not event_loop:
            event_loop = asyncio.get_event_loop()
        return Loop(
            func, loop=event_loop, seconds=seconds, minutes=minutes, hours=hours
        )

    return decorator
