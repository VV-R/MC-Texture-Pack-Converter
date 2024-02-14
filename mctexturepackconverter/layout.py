from collections.abc import Iterator


class Layout:
    def __init__(self, layout):
        self.layout = layout

    layout: list[str]

    def width(self):
        return max(len(row) for row in self.layout)

    def height(self):
        return len(self.layout)

    def iter_elements(self) -> Iterator[int, int, str]:
        for i, row in enumerate(self.layout):
            for j, block in enumerate(row):
                yield i, j, block
