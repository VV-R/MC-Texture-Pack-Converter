# Todo:
#   logo.png
#   particles.png
#   slot.png
#   Fix pig nose texture
#   Add legs to bed

from argparse import ArgumentParser
from pathlib import Path
import functools
from typing import Iterator

from PIL import Image

import paintings
from liquid import copy_water, copy_lava
from texture_collection import convert_texture_collection
from copy_files import (
    mk_dirs, process_from_to_list, gui_files_copy_list,
    entity_files_copy_list, armor_files_copy_list, environment_files_copy_list
)
from get_base import get_base
from texture_collection import TerrainTextureBuilder, ItemsTextureBuilder
from items import items
from terrain import terrain
from pipeline.pipelines import substitution_pipeline
from pipeline import Context
from pipeline.middleware.callback_middleware import CallbackMiddleware
from pipeline.middleware.raise_middleware import RaiseMiddleware
from bed import convert_bed
from chest import convert_chest


argparser = ArgumentParser()
argparser.add_argument('sources', type=Path, nargs='+')
argparser.add_argument('destination', type=Path)
argparser.add_argument(
    '-s', '--skip-missing', action='store_true', help='skip missing textures'
)
argparser.add_argument(
    '--bed-color', help='select bed color', default='red', choices=[
        'black', 'blue', 'brown', 'cyan', 'gray', 'green', 'light_blue',
        'light_gray', 'lime', 'magenta', 'orange', 'pink', 'purple', 'red',
        'white', 'yellow'
    ]
)

def get_terrain_texture_builder(base: int) -> TerrainTextureBuilder:
    return TerrainTextureBuilder.from_texture_info(
        base, terrain.width(), terrain.height()
    )


def get_items_texture_builder(base: int) -> ItemsTextureBuilder:
    return ItemsTextureBuilder.from_texture_info(
        base, items.width(), items.height()
    )


def join_path_to_sources(
    sources: list[tuple[Path, int]], path: Path | str
) -> Iterator[tuple[Path, int]]:
    return ((p / path, b) for p, b in sources)


def do_paintings(
    base: int,
    sources: list[tuple[Path, int]]
):
    image = paintings.get_image(base)
    pipeline = substitution_pipeline.factory(
        *join_path_to_sources(sources, 'assets/minecraft/textures/painting')
    )
    paintings.convert_paintings(base, image, pipeline)

    back_texture = pipeline.next(Context('back', 0, 0, base, base))
    if back_texture is None:
        return image

    try:
        paintings.apply_back_texture(base, image, back_texture)
    finally:
        back_texture.close()
    return image


def handle_sources(sources: list[Path]) -> list[tuple[Path, int]]:
    result = []
    for source in sources:
        result.append((source, get_base(source)))
    return result


def main():
    args = argparser.parse_args()
    args.destination.mkdir(exist_ok=True)

    sources = handle_sources(args.sources)

    base = sources[0][1]

    pipeline_block = substitution_pipeline.factory(*join_path_to_sources(
        sources, "assets/minecraft/textures/block/"
    ))


    pipeline_item = substitution_pipeline.factory(*join_path_to_sources(
        sources, "assets/minecraft/textures/item/"
    ))

    pipeline_bed = substitution_pipeline.factory(*join_path_to_sources(
        sources, 'assets/minecraft/textures/entity/bed'
    ))

    pipeline_chest = substitution_pipeline.factory(*join_path_to_sources(
        sources, 'assets/minecraft/textures/entity/chest'
    ))

    if not args.skip_missing:
        raise_middleware = RaiseMiddleware(
            lambda c: Exception(f'Could not find texture {c.kind}')
        )
        pipeline_block.add(raise_middleware)
        pipeline_item.add(raise_middleware)
        pipeline_bed.add(raise_middleware)
        pipeline_chest.add(raise_middleware)

    terrain_builder = get_terrain_texture_builder(base)

    chest_texture = pipeline_chest.next(Context("normal", 0, 0, base, base))
    chest_texture_left = pipeline_chest.next(Context("normal_left", 0, 0, base, base))
    chest_texture_right = pipeline_chest.next(Context("normal_right", 0, 0, base, base))
    convert_chest(terrain_builder, chest_texture, chest_texture_left, chest_texture_right)

    bed_texture = pipeline_bed.next(Context(args.bed_color, 0, 0, base, base));
    convert_bed(terrain_builder, bed_texture)

    water = pipeline_block.next(Context('water_still', 0, 0, base, base))
    if water:
        copy_water(
            water,
            terrain_builder, base=base
        )
    lava = pipeline_block.next(Context('lava_still', 0, 0, base, base))
    if lava:
        copy_lava(
            lava,
            terrain_builder, base=base
        )

    convert_texture_collection(terrain, terrain_builder, base, pipeline_block)

    items_builder = get_items_texture_builder(base)
    convert_texture_collection(items, items_builder, base, pipeline_item)

    mk_dirs(args.destination)
    process_from_to_list(args.sources[0], args.destination, gui_files_copy_list, args.skip_missing)
    process_from_to_list(args.sources[0], args.destination, entity_files_copy_list, args.skip_missing)
    process_from_to_list(args.sources[0], args.destination, armor_files_copy_list, args.skip_missing)
    process_from_to_list(args.sources[0], args.destination, environment_files_copy_list, args.skip_missing)

    terrain_builder.save(args.destination / 'terrain.png')
    items_builder.save(args.destination / 'gui/items.png');

    paintings = do_paintings(base, sources)
    paintings.save(args.destination / 'art/kz.png')

if __name__ == '__main__':
    main()
