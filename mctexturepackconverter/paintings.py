from pathlib import Path

from PIL import Image

from pipeline import Context


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Painting:
    def __init__(self, name: str, x: int, y: int, w: int, h: int):
        self.name = name
        self.position = Position(x, y)
        self.w = w
        self.h = h


paintings = [
    Painting('kebab', 0, 0, 16, 16),
    Painting('aztec', 1, 0, 16, 16),
    Painting('alban', 2, 0, 16, 16),
    Painting('aztec2', 3, 0, 16, 16),
    Painting('bomb', 4, 0, 16, 16),
    Painting('plant', 5, 0, 16, 16),
    Painting('wasteland', 6, 0, 16, 16),
    Painting('pool', 0, 2, 32, 16),
    Painting('courbet', 2, 2, 32, 16),
    Painting('sea', 4, 2, 32, 16),
    Painting('sunset', 6, 2, 32, 16),
    Painting('creebet', 8, 2, 32, 16),
    Painting('wanderer', 0, 4, 16, 32),
    Painting('graham', 1, 4, 16, 32),
    Painting('fighters', 0, 6, 64, 32),
    Painting('match', 0, 8, 32, 32),
    Painting('bust', 2, 8, 32, 32),
    Painting('stage', 4, 8, 32, 32),
    Painting('void', 6, 8, 32, 32),
    Painting('skull_and_roses', 8, 8, 32, 32),
    Painting('pointer', 0, 12, 64, 64),
    Painting('pigscene', 4, 12, 64, 64),
    Painting('burning_skull', 8, 12, 64, 64),
    Painting('skeleton', 12, 4, 64, 48),
    Painting('donkey_kong', 12, 7, 64, 48)
]


def get_image(base):
    return Image.new('RGBA', (16 * base, 16 * base), (255, 255, 255, 0))


def convert_paintings(base, image, pipeline):
    m = base // 16

    for painting in paintings:
        src_image = pipeline.next(
            Context(painting.name, 0, 0, m * painting.w, m * painting.h)
        )
        if src_image is None:
            continue

        try:
            image.paste(
                src_image,
                box=(painting.position.x * base, painting.position.y * base)
            )
        finally:
            src_image.close()


def apply_back_texture(base, image, back_image):
    for x in range(12 * base, 16 * base, base):
        for y in range(0, 4 * base, base):
            image.paste(back_image, box=(x, y))


if __name__ == '__main__':
    image = get_image(32)
    convert_paintings(32, image, Path('texturepack/assets/minecraft/textures/painting/'))
    apply_back_texture(32, image, Image.open(Path('texturepack/assets/minecraft/textures/painting/back.png')))
    image.save("kz.png")
