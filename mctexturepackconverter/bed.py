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
    back.paste(img.crop((
        spacing, spacing, spacing + builder.base,
        spacing + thickness
    )), (0, builder.scale(7)))

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

    for x, y, part in (
        (6, 8, top_lower),
        (7, 8, top_head),
        (5, 9, back),
        (6, 9, side_lower),
        (7, 9, side_head),
        (8, 9, front)
    ):
        builder.put(x, y, part)
