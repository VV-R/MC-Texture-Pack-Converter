from .pipeline.pipelines import substitution_pipeline
from .pipeline import Context
from .terrain import terrain
from .get_base import get_base

from pathlib import Path
import sys


packs = [
    ((path / "assets/minecraft/textures/block/"), get_base(path))
    for path in (Path(sys.argv[1]), Path(sys.argv[2]))
]

print(packs)

pipeline = substitution_pipeline.factory(*packs)


count = 0


item_set = set()

for i, j, item in filter(lambda x: x[2] != "", terrain.iter_elements()):
    print(item)

    item_set.add(item)

    img = pipeline.next(Context(item, i, j))
    count += 1
    if count >= float(20):
        break

    if 'leave' in item:
        print(f'{item=}')
        print(f'{img=}')

    if img:
        img.show()
        pass
    else:
        print("img is None")

print(item_set)
print(len(item_set))
