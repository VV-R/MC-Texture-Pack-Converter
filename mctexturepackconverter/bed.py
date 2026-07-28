from PIL import Image

def convert_bed(builder, img):
    thickness = builder.scale(6)
    top_head = img.crop((
        thickness, thickness, thickness + builder.base,
        thickness + builder.base
    )).rotate(-90)

    top_lower = img.crop((
        thickness,
        2 * thickness + builder.base,
        thickness + builder.base,
        2 * thickness + 2 * builder.base
    ))

    spacing = builder.scale(22)
    back = builder.blank_item()
    back.paste(
        img.crop((
            spacing, spacing, spacing + builder.base,
            spacing + thickness
        )).transpose(method=Image.Transpose.ROTATE_180),
        (0, builder.scale(7))
    )

    front = builder.blank_item()

    front.paste(img.crop((
        thickness, 0, builder.scale(22), thickness
    )).transpose(
        method=Image.Transpose.ROTATE_180
    ), (0, builder.scale(7)))

    side_head = builder.blank_item()
    side_head.paste(
        img.crop((
            builder.scale(22), builder.scale(6),
            builder.scale(28), builder.scale(22)
        )).transpose(method=Image.Transpose.ROTATE_270),
        (0, builder.scale(7))
    )

    side_lower = builder.blank_item()
    side_lower.paste(
        img.crop((
            builder.scale(22), builder.scale(28),
            builder.scale(28), builder.scale(44) 
        )).transpose(method=Image.Transpose.ROTATE_270),
        (0, builder.scale(7))
    )

    # copy and paste bed leg textures
    # Left leg on front side
    front.paste(
        img.crop((
            builder.scale(53), builder.scale(21),
            builder.scale(56), builder.scale(24)
        )),
        (builder.scale(0), builder.scale(13))
    )

    # Right leg on front side
    front.paste(
        img.crop((
            builder.scale(50), builder.scale(9),
            builder.scale(53), builder.scale(12)
        )),
        (builder.scale(13), builder.scale(13))
    )

    # Left leg on back side
    back.paste(
        img.crop((
            builder.scale(53), builder.scale(3),
            builder.scale(56), builder.scale(6)
        )),
        (builder.scale(0), builder.scale(13))
    )

    # Right leg on back side
    back.paste(
        img.crop((
            builder.scale(50), builder.scale(15),
            builder.scale(53), builder.scale(18)
        )),
        (builder.scale(13), builder.scale(13))
    )

    # Right leg on left and right side
    side_head.paste(
        img.crop((
            builder.scale(50), builder.scale(21),
            builder.scale(53), builder.scale(24)
        )),
        (builder.scale(13), builder.scale(13))
    )

    # Left leg on left and right side
    side_lower.paste(
        img.crop((
            builder.scale(53), builder.scale(15),
            builder.scale(56), builder.scale(18)
        )),
        (builder.scale(0), builder.scale(13))
    )

    for x, y, part in (
        (6, 8, top_lower),
        (7, 8, top_head),
        (5, 9, back),
        (6, 9, side_lower),
        (7, 9, side_head),
        (8, 9, front)
    ):
        builder.put(x, y, part)
