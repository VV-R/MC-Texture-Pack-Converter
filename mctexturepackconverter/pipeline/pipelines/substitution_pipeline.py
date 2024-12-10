from pathlib import Path
import itertools

from ..pipeline import Pipeline
from ..middleware.from_resourcepack import FromResourcepack
from ..middleware.scale_middleware import ScaleMiddleware


def factory(*entries: tuple[tuple[Path, int]]) -> Pipeline:
    # first value in tuple is a path and the second in the texture base

    if len(entries) == 1:
        return Pipeline(FromResourcepack(entries[0][0]))

    final_base = entries[0][1]

    highest_base = max(b for _, b in entries)

    assert highest_base == final_base, \
        "Scaling larger res textures down is not supported"

    pipeline = Pipeline(*(
        FromResourcepack(path) for path, _ in
        itertools.islice(reversed(entries), len(entries) - 1)
    ))

    lowest_base = min(b for _, b in entries)
    if final_base > lowest_base:
        pipeline.add(ScaleMiddleware())

    pipeline.add(FromResourcepack(entries[0][0]))

    return pipeline
