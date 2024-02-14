def convert_bed(terrain, source, color='red'):
    with Image.open(source / (color + '.png')) as img:
        thickness = terrain.scale(6)
        top_head = img.crop((
            thickness, thickness, thickness + terrain.base,
            thickness + terrain.base
        )).rotate(-90)

        top_lower = img.crop((
            thickness,
            2 * thickness + terrain.base,
            thickness + terrain.base,
            2 * thickness + 2 * terrain.base
        ))

        spacing = terrain.scale(22)
        back = terrain.blank_item()
        back.paste(img.crop((
            spacing, spacing, spacing + terrain.base,
            spacing + thickness
        )), (0, terrain.scale(7)))

        front = terrain.blank_block()

        front.paste(img.crop((
            thickness, 0, terrain.scale(22), thickness
        )).transpose(
            method=Image.Transpose.ROTATE_180
        ), (0, terrain.scale(7)))

        side_head = terrain.blank_item()
        side_head.paste(
            img.crop((
                terrain.scale(22), terrain.scale(6),
                terrain.scale(28), terrain.scale(22)
            )).transpose(method=Image.Transpose.ROTATE_270),
            (0, terrain.scale(7))
        )

        side_lower = terrain.blank_block()
        side_lower.paste(
            img.crop((
                terrain.scale(22), terrain.scale(28),
                terrain.scale(28), terrain.scale(44) 
            )).transpose(method=Image.Transpose.ROTATE_270),
            (0, terrain.scale(7))
        )

        for x, y, part in (
            (6, 8, top_lower),
            (7, 8, top_head),
            (5, 9, back),
            (6, 9, side_lower),
            (7, 9, side_head),
            (8, 9, front)
        ):
            terrain.put(x, y, part)
