from abc import ABC, abstractmethod
import functools
from pathlib import Path

from PIL import Image

from terrain import terrain
from items import items
from utils import COULD_NOT_FIND_MSG
from pipeline import Context
from pipeline.middleware.callback_middleware import CallbackMiddleware


class TextureCollectionBuilder(ABC):
    def __init__(self, base, img):
        self.base = base
        self.img = img

    @classmethod
    def from_texture_info(cls, base: int, width: int, height: int):
        return cls(
            base,
            Image.new('RGBA', (width * base, height * base), (255, 255, 255, 0))
        )

    def put(self, x, y, img: Image):
        self.img.paste(img, box=(x * self.base, y * self.base))

    def save(self, path):
        self.img.save(path)

    def scale(self, v: int) -> int:
        return self.base // 16 * v

    @abstractmethod
    def blank_item(self):
        pass


class TerrainTextureBuilder(TextureCollectionBuilder):
    def blank_item(self):
        return Image.new(
            'RGBA', (self.base, self.base),
            (255, 255, 255, 0)
        )


class ItemsTextureBuilder(TextureCollectionBuilder):
    def blank_item(self):
        return Image.new(
            'RGBA', (self.base, self.base),
            (255, 255, 255, 0)
        )


def convert_texture_collection(layout, builder, base, pipeline):
    it = filter(lambda x: x[2] != '', layout.iter_elements())

    def handle_img(context, img):
        if img is None:
            return

        if img.height != builder.base:
            img = img.crop((0, 0, base, base))
        builder.put(context.j, context.i, img)
        img.close()

    pipeline.add(CallbackMiddleware(handle_img))

    for i, j, item in it:
        img = pipeline.next(Context(item, i, j, base, base))
    return builder
