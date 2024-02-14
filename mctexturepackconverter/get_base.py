from pathlib import Path

from PIL import Image


def get_base(source: Path) -> int:
    with Image.open(
        source / 'assets/minecraft/textures/block/dirt.png'
    ) as img:
        return img.width
