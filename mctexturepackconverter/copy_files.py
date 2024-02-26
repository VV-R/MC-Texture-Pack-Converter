import shutil
import os

from utils import COULD_NOT_FIND_MSG


class FromTo:
    def __init__(self, dest: str, to: str):
        self.dest = dest
        self.to = to

    def copy(self, source, destination, skip_missing=False):
        try:
            shutil.copy(
                os.path.join(source, self.dest),
                os.path.join(destination, self.to)
            )
        except FileNotFoundError:
            if not skip_missing:
                raise
            print(COULD_NOT_FIND_MSG.format(self.dest))


dirs = [
    'gui',
    'mob',
    'armor',
    'environment',
    'art'
]


gui_files_copy_list = [
    FromTo('assets/minecraft/textures/gui/widgets.png', 'gui/gui.png'),
    FromTo('assets/minecraft/textures/gui/container/crafting_table.png', 'gui/crafting.png'),
    FromTo('assets/minecraft/textures/gui/container/furnace.png', 'gui/furnace.png'),
    FromTo('assets/minecraft/textures/gui/container/generic_54.png', 'gui/container.png'),
    FromTo('assets/minecraft/textures/gui/container/inventory.png', 'gui/inventory.png'),
    FromTo('assets/minecraft/textures/gui/container/dispenser.png', 'gui/trap.png'),
    FromTo('assets/minecraft/textures/gui/icons.png', 'gui/icons.png')
]


entity_files_copy_list = [
    FromTo('assets/minecraft/textures/entity/steve.png', 'mob/char.png'),
    FromTo('assets/minecraft/textures/entity/chicken.png', 'mob/chicken.png'),
    FromTo('assets/minecraft/textures/entity/cow/cow.png', 'mob/cow.png'),
    FromTo('assets/minecraft/textures/entity/creeper/creeper.png', 'mob/creeper.png'),
    FromTo('assets/minecraft/textures/entity/ghast/ghast.png', 'mob/ghast.png'),
    FromTo('assets/minecraft/textures/entity/ghast/ghast_shooting.png', 'mob/ghast_fire.png'),
    FromTo('assets/minecraft/textures/entity/pig/pig.png', 'mob/pig.png'),
    FromTo('assets/minecraft/textures/entity/piglin/zombified_piglin.png', 'mob/pigzombie.png'),
    FromTo('assets/minecraft/textures/entity/pig/pig_saddle.png', 'mob/saddle.png'),
    FromTo('assets/minecraft/textures/entity/sheep/sheep_fur.png', 'mob/sheep_fur.png'),
    FromTo('assets/minecraft/textures/entity/sheep/sheep.png', 'mob/sheep.png'),
    FromTo('assets/minecraft/textures/entity/silverfish.png', 'mob/silverfish.png'),
    FromTo('assets/minecraft/textures/entity/skeleton/skeleton.png', 'mob/skeleton.png'),
    FromTo('assets/minecraft/textures/entity/slime/slime.png', 'mob/slime.png'),
    FromTo('assets/minecraft/textures/entity/spider_eyes.png', 'mob/spider_eyes.png'),
    FromTo('assets/minecraft/textures/entity/spider/spider.png', 'mob/spider.png'),
    FromTo('assets/minecraft/textures/entity/wolf/wolf_angry.png', 'mob/wolf_angry.png'),
    FromTo('assets/minecraft/textures/entity/wolf/wolf.png', 'mob/wolf.png'),
    FromTo('assets/minecraft/textures/entity/wolf/wolf_tame.png', 'mob/wolf_tame.png'),
    FromTo('assets/minecraft/textures/entity/zombie/zombie.png', 'mob/zombie.png')
]

armor_files_copy_list = [
    FromTo('assets/minecraft/textures/models/armor/chainmail_layer_1.png', 'armor/chain_1.png'),
    FromTo('assets/minecraft/textures/models/armor/chainmail_layer_2.png', 'armor/chain_2.png'),
    FromTo('assets/minecraft/textures/models/armor/diamond_layer_1.png', 'armor/diamond_1.png'),
    FromTo('assets/minecraft/textures/models/armor/diamond_layer_2.png', 'armor/diamond_2.png'),
    FromTo('assets/minecraft/textures/models/armor/gold_layer_1.png', 'armor/gold_1.png'),
    FromTo('assets/minecraft/textures/models/armor/gold_layer_2.png', 'armor/gold_2.png'),
    FromTo('assets/minecraft/textures/models/armor/iron_layer_1.png', 'armor/iron_1.png'),
    FromTo('assets/minecraft/textures/models/armor/iron_layer_2.png', 'armor/iron_2.png'),
    FromTo('assets/minecraft/textures/models/armor/leather_layer_1.png', 'armor/cloth_1.png'),
    FromTo('assets/minecraft/textures/models/armor/leather_layer_2.png', 'armor/cloth_2.png')
]

# Add sun and moon later
environment_files_copy_list = [
    FromTo('assets/minecraft/textures/environment/rain.png', 'environment/rain.png'),
    FromTo('assets/minecraft/textures/environment/snow.png', 'environment/snow.png'),
    FromTo('assets/minecraft/textures/environment/clouds.png', 'environment/clouds.png')
]


def process_from_to_list(source, destination, collection, skip_missing=False):
    for from_to in collection:
        from_to.copy(source, destination, skip_missing)


def mk_dirs(destination):
    for dir in dirs:
        os.makedirs(os.path.join(destination, dir))
