# Todo:
#   logo.png
#   particles.png
#   slot.png
#   unknown_pack.png
#   Fix pig nose texture
#   Finish bed support.
#   Fix invisible door and chest.

from argparse import ArgumentParser
from pathlib import Path
import functools

from PIL import Image

import paintings
from liquid import copy_water, copy_lava
from texture_collection import convert_blocks, convert_items
from copy_files import (
    mk_dirs, process_from_to_list, gui_files_copy_list,
    entity_files_copy_list, armor_files_copy_list, environment_files_copy_list
)
from get_base import get_base


argparser = ArgumentParser()
argparser.add_argument('source', type=Path)
argparser.add_argument('destination', type=Path)
argparser.add_argument(
    '-s', '--skip-missing', action='store_true', help='skip missing textures'
)


def do_paintings(
    base: int,
    source: Path
):
    image = paintings.get_image(base)
    paintings.convert_paintings(base, image, source)
    paintings.apply_back_texture(base, image, Image.open(source / 'back.png'))
    return image


def main():
    args = argparser.parse_args()
    args.destination.mkdir(exist_ok=True)
    base = get_base(args.source)
    terrain_builder = convert_blocks(args.source / 'assets/minecraft/textures/block', skip_missing=args.skip_missing)
    items_builder = convert_items(args.source / 'assets/minecraft/textures/item', skip_missing=args.skip_missing)
    #convert_bed(terrain, args.source / 'assets/minecraft/textures/entity/bed')
    mk_dirs(args.destination)
    process_from_to_list(args.source, args.destination, gui_files_copy_list, args.skip_missing)
    process_from_to_list(args.source, args.destination, entity_files_copy_list, args.skip_missing)
    process_from_to_list(args.source, args.destination, armor_files_copy_list, args.skip_missing)
    process_from_to_list(args.source, args.destination, environment_files_copy_list, args.skip_missing)
    copy_water(
        args.source / 'assets/minecraft/textures/block/water_still.png',
        terrain_builder, base=base
    )
    copy_lava(
        args.source / 'assets/minecraft/textures/block/lava_still.png',
        terrain_builder, base=base
    )
    terrain_builder.save(args.destination / 'terrain.png')
    items_builder.save(args.destination / 'gui/items.png');

    paintings = do_paintings(base, args.source / 'assets/minecraft/textures/painting')
    paintings.save(args.destination / 'art/kz.png')

if __name__ == '__main__':
    main()
