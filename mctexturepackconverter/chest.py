from PIL import Image

from texture_collection import TerrainTextureBuilder

def build_front(img, alt_base: int, builder: TerrainTextureBuilder) -> None:
    front_lid = img.crop((3 * alt_base, alt_base, 4 * alt_base, alt_base // 14 * 19))
    front = Image.new('RGB', (builder.base, builder.base))
    front.paste(front_lid, (builder.base // 16, builder.base // 16))

    front_body = img.crop((3 * alt_base, alt_base // 14 * 33, 4 * alt_base, alt_base // 14 * 42))
    front_body = front_body.rotate(180)
    front.paste(front_body, (builder.base // 16, builder.base // 16 + front_lid.height))

    lock = img.crop((
        alt_base // 14 * 4, alt_base // 14 * 2,
        alt_base // 14 * 6, alt_base // 14 * 5
    ))
    front.paste(lock, (alt_base // 14 * 7, alt_base // 14 * 4))

    builder.put(11, 1, front)


def build_back(img, alt_base: int, builder: TerrainTextureBuilder) -> None:
    back = Image.new('RGB', (builder.base, builder.base))

    back_lid = img.crop((alt_base, alt_base, alt_base * 2, alt_base // 14 * 19))
    back.paste(back_lid, (builder.base // 16, builder.base // 16))
    back_body = img.crop((alt_base, alt_base // 14 * 33, alt_base * 2, alt_base // 14 * 42))
    back_body = back_body.rotate(180)
    back.paste(back_body, (builder.base // 16, builder.base // 16 + back_lid.height))
    builder.put(10, 1, back)

def build_top(img, alt_base: int, builder: TerrainTextureBuilder) -> None:
    top = Image.new('RGB', (builder.base, builder.base))

    top_body = img.crop((alt_base * 2, 0, alt_base * 3, alt_base))
    top.paste(top_body, (builder.base // 16, builder.base // 16))
    builder.put(9, 1, top)

def build_front_double(
    img,
    alt_base: int,
    builder: TerrainTextureBuilder,
    offset_x: int,
) -> None:
    front_left = Image.new('RGB', (builder.base, builder.base))

    front_left_body = img.crop((alt_base // 14 * 43, alt_base // 14 * 33, alt_base // 14 * 58, alt_base // 14 * 43))
    front_left_body = front_left_body.rotate(180)
    front_left.paste(front_left_body, (offset_x, builder.base // 16 * 5))

    front_left_lid = img.crop((
        alt_base // 14 * 43, alt_base,
        alt_base // 14 * 58, alt_base // 14 * 19
    )).rotate(180)
    front_left.paste(front_left_lid, (offset_x, builder.base // 16))
    return front_left

def build_front_left(img, alt_base: int, builder: TerrainTextureBuilder) -> None:
    side = build_front_double(img, alt_base, builder, 0)
    builder.put(10, 2, side)


def build_front_right(img, alt_base: int, builder: TerrainTextureBuilder) -> None:
    side = build_front_double(img, alt_base, builder, builder.base // 16)
    builder.put(9, 2, side)

def convert_chest(builder: TerrainTextureBuilder, img, left, right) -> None:
    # a chest texture is 7/8 the dimensions of a regular block
    alt_base = builder.base // 8 * 7
    build_front(img, alt_base, builder)
    build_back(img, alt_base, builder)
    build_top(img, alt_base, builder)
    build_front_left(left, alt_base, builder)
    build_front_right(right, alt_base, builder)
