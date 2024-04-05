from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

from PIL import Image

from utils import COULD_NOT_FIND_MSG


class AbstractImageProvider(ABC):
    @abstractmethod
    def do_with(self, path: Path, callback: Callable[[Image], None]) -> None:
        raise NotImplementedError()


class ImageProvider(AbstractImageProvider):
    def __init__(self, source: Path) -> None:
        self._source = source

    def do_with(self, path: Path, callback: Callable[[Image], None]) -> None:
        with Image.open(self._source / path) as img:
            callback(img)


class SkippingImageProvider(ImageProvider):
    def do_with(self, path: Path, callback: Callable[[Image], None]) -> None:
        try:
            super().do_with(path, callback)
        except FileNotFoundError:
            print(COULD_NOT_FIND_MSG.format(path))
