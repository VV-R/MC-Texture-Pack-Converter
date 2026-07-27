from pathlib import Path
from typing import Callable

from PIL import Image

from .. import AbstractMiddleware, Context


ImageType = Image.Image


class FromResourcepack(AbstractMiddleware):
    def __init__(self, path: Path) -> None:
        self._path = path

    def _try_path(self, path: str) -> ImageType | None:
        try:
            return Image.open(self._path / f'{path}.png')
        except FileNotFoundError:
            pass
        if (dir_path := self._path / f'{path}').is_dir():
            try:
                # NOTE: maybe look for other files?
                return Image.open(dir_path / '0.png')
            except FileNotFoundError:
                return None
        return None

    def next(
        self, next_: Callable[[Context], ImageType | None], context: Context
    ) -> ImageType | None:
        if (img := self._try_path(context.kind)):
            return img

        '''
        Some resourcepacks have certain textures grouped in folders and
        others don't. For example "oak_leaves.png" vs
        "leaves/oak_leaves.png". This code block handles such possibilities.
        '''
        split = context.kind.split('/')
        if len(split) > 1 and (img := self._try_path(split[-1])):
            return img

        return next_(context) if next_ is not None else None
