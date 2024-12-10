import functools
from abc import ABC, abstractmethod
from typing import Callable
from pathlib import Path
from dataclasses import dataclass

from PIL import Image


@dataclass(slots=True)
class Context:
    kind: str
    i: int
    j: int
    w: int
    h: int


class AbstractMiddleware:
    @abstractmethod
    def next(
        self, next_: Callable[[Context], Image.Image | None], context: Context
    ) -> Image.Image | None:
        ...


class Pipeline:
    def __init__(self, *middleware) -> None:
        if len(middleware) == 0:
            raise ValueError("You must provide at least one middleware")
        self._setup_pipeline(middleware)

    def _setup_pipeline(self, middleware) -> None:
        it = iter(middleware)
        m = next(it)
        self._entry = functools.partial(m.next, None)

        for m in it:
            self.add(m)

    def add(self, middleware: AbstractMiddleware) -> None:
        self._entry = functools.partial(middleware.next, self._entry)

    def next(self, context: Context) -> Image.Image | None:
        return self._entry(context)
