from typing import Callable

from PIL import Image

from .. import AbstractMiddleware, Context


ImageType = Image.Image


class RaiseMiddleware(AbstractMiddleware):
    def __init__(self, factory: Callable[[Context], Exception]) -> None:
        self._factory = factory

    def next(
        self, next_: Callable[[Context], ImageType | None], context: Context
    ) -> ImageType | None:
        img = next_(context)
        if img is None:
            raise self._factory(context)
        return img
