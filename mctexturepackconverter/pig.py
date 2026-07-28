def convert_pig(builder, img):
    nose = img.crop((
        builder.scale(16), builder.scale(17),
        builder.scale(22), builder.scale(20)
    ))
    img.paste(nose, (builder.scale(9), builder.scale(12)))
    return img
