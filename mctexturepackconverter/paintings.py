from pathlib import Path

from PIL import Image


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Painting:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.position = Position(x, y)


paintings = [
    Painting('kebab', 0, 0),
    Painting('aztec', 1, 0),
    Painting('alban', 2, 0),
    Painting('aztec2', 3, 0),
    Painting('bomb', 4, 0),
    Painting('plant', 5, 0),
    Painting('wasteland', 6, 0),
    Painting('pool', 0, 2),
    Painting('courbet', 2, 2),
    Painting('sea', 4, 2),
    Painting('sunset', 6, 2),
    Painting('creebet', 8, 2),
    Painting('wanderer', 0, 4),
    Painting('graham', 1, 4),
    Painting('fighters', 0, 6),
    Painting('fighters', 0, 6),
    Painting('match', 0, 8),
    Painting('bust', 2, 8),
    Painting('stage', 4, 8),
    Painting('void', 6, 8),
    Painting('skull_and_roses', 8, 8),
    Painting('pointer', 0, 12),
    Painting('pigscene', 4, 12),
    Painting('burning_skull', 8, 12),
    Painting('skeleton', 12, 4),
    Painting('donkey_kong', 12, 7)
]


def get_image(base):
    return Image.new('RGBA', (16 * base, 16 * base), (255, 255, 255, 0))


def convert_paintings(base, image, source):
    for painting in paintings:
        with Image.open(source / f'{painting.name}.png') as src_image:
            image.paste(
                src_image,
                box=(painting.position.x * base, painting.position.y * base)
            )


def apply_back_texture(base, image, back_image):
    for x in range(12 * base, 16 * base, base):
        for y in range(0, 4 * base, base):
            image.paste(back_image, box=(x, y))


if __name__ == '__main__':
    image = get_image(32)
    convert_paintings(32, image, Path('texturepack/assets/minecraft/textures/painting/'))
    apply_back_texture(32, image, Image.open(Path('texturepack/assets/minecraft/textures/painting/back.png')))
    image.save("kz.png")
