# McTexturepackConverter

Is a tool to convert modern minecraft resource packs to minecraft b.1.7.3
texturepacks (maybe even older versions, but I don't really know how compatible
those are).

## Dependencies

- Python3
- Pillow package for python3.

## Usage

`python mctexturepackconverter {path to resource pack (must be unzipped)} {path to output directory}`

It is also possible to make the program fall back on another resource pack if
the first one does not have the texture:
`python mctexturepackconverter {path to resource pack} {path to second resource pack} {path to output directory}`.
You can chain as many resource packs as you like.
Note that chaining does not work for entities and gui textures (yet).

You can use the -s flag to make the program skip missing textures instead of
raising an exception.

After converting the texturepack, zip the contents of the output folder.
Example using the zip command:

```
cd output_folder

zip ../texturepack.zip -r ./*

cd -
```

That's all, just place it in your minecraft texturepack folder, open the game and
load the texturepack.

## License

This program is released under AGPL-3.0-only.
