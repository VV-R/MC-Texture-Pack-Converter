import itertools
import functools

from PIL import Image


def _copy_liquid(x_cords, y_cords, source, terrain, base):
    with Image.open(source) as img:
        for i, x, y in zip(
            itertools.count(),
            x_cords,
            y_cords
        ):
            cropped = img.crop((
                0, i * base,
                base, (i + 1) * base
            ))
            terrain.put(
                x, y,
                cropped
            )

copy_water = functools.partial(
    _copy_liquid,
    [13, 14, 15, 14, 15],
    [12, 12, 12, 13, 13]
)

copy_lava = functools.partial(
    _copy_liquid,
    [13, 14, 15, 14, 15],
    [14, 14, 14, 15, 15]
)
