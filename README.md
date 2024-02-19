# McTexturepackConverter

Is a tool to convert modern minecraft resource packs to minecraft b.1.7.3
texturepacks (maybe even older versions, but I don't really know how compatible
those are).

## Dependencies

- Python3
- Pillow package for python3.

## Usage

`python mctexturepackconverter {path to resource pack (must be unzipped)} {path to output directory}`

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
