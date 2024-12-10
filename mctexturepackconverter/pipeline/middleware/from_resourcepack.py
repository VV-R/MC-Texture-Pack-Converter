from pathlib import Path
from typing import Callable

from PIL import Image

from .. import AbstractMiddleware, Context


ImageType = Image.Image


class FromResourcepack(AbstractMiddleware):
    def __init__(self, path: Path) -> None:
        self._path = path

    def next(
        self, next_: Callable[[Context], ImageType | None], context: Context
    ) -> ImageType | None:
        try:
            return Image.open(self._path / f'{context.kind}.png')
        except FileNotFoundError:
            pass
        try:
            split = context.kind.split('/')
            if len(split) > 1:
                return Image.open(self._path / f'{split[-1]}.png')
        except FileNotFoundError:
            pass
        return next_(context) if next_ is not None else None
