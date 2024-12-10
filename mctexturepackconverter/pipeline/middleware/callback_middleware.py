from typing import Callable

from PIL import Image

from .. import AbstractMiddleware, Context

ImageType = Image.Image

class CallbackMiddleware(AbstractMiddleware):
    def __init__(self, callback: lambda _: None) -> None:
        self.callback = callback

    def next(
        self, next_: Callable[[Context], ImageType | None], context: Context
    ) -> ImageType | None:
        img = next_(context)
        self.callback(context, img)
        return img
