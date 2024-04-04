from abc import ABC, abstractmethod
import functools

from PIL import Image

from terrain import terrain
from items import items
from utils import COULD_NOT_FIND_MSG


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


def _convert_texture_collection(
    layout, texture_builder, source, base, skip_missing: bool = False
):
    it = filter(lambda x: x[2] != '', layout.iter_elements())

    builder = texture_builder.from_texture_info(
        base, layout.width(), layout.height()
    )

    for i, j, item in it:
        try:
            with Image.open(source / (item + '.png')) as img:
                if img.height != builder.base:
                    img = img.crop((0,0, builder.base, builder.base))
                if img.width != builder.base:
                    print(f'Skip {item}.png, because of deviating image size')
                    continue
                builder.put(j, i, img)
        except FileNotFoundError:
            if skip_missing:
                print(COULD_NOT_FIND_MSG.format(f'{item}.png'))
            else:
                raise

    return builder


convert_blocks = functools.partial(
    _convert_texture_collection, terrain, TerrainTextureBuilder
)

convert_items = functools.partial(
    _convert_texture_collection, items, ItemsTextureBuilder
)
