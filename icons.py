# Hub menu icons for the MCDistrict pack: Squid Game guard mask, GTA police car, AnarchyPvP logo (server icon).
# Pixel art drawn at 32 x 32; the logo keeps its 64 x 64 server icon. Called by gen.py before zipping.
import json, os, shutil
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))


def squid():
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((3, 1, 28, 31), fill=(214, 46, 110, 255))          # pink hood
    d.ellipse((5, 3, 26, 29), fill=(232, 72, 132, 255))
    d.ellipse((8, 7, 23, 27), fill=(18, 18, 22, 255))            # black mask
    d.ellipse((9, 8, 18, 15), fill=(40, 40, 48, 255))            # mask shine
    d.ellipse((11, 12, 20, 21), outline=(245, 245, 245, 255), width=2)  # the circle symbol
    d.line((10, 4, 13, 2), fill=(250, 140, 180, 255))            # hood highlight
    return im


def copcar():
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((2, 15, 29, 22), fill=(20, 22, 30, 255))          # lower body (black)
    d.polygon([(8, 15), (11, 9), (21, 9), (24, 15)], fill=(235, 235, 240, 255))  # white cabin
    d.polygon([(10, 14), (12, 10), (15, 10), (15, 14)], fill=(120, 170, 220, 255))  # windows
    d.polygon([(17, 14), (17, 10), (20, 10), (22, 14)], fill=(120, 170, 220, 255))
    d.rectangle((2, 15, 29, 17), fill=(235, 235, 240, 255))       # white stripe on the doors
    d.rectangle((12, 7, 14, 8), fill=(220, 30, 30, 255))          # light bar red / blue
    d.rectangle((17, 7, 19, 8), fill=(30, 80, 230, 255))
    d.rectangle((15, 7, 16, 8), fill=(200, 200, 205, 255))
    d.rectangle((28, 18, 29, 19), fill=(255, 230, 120, 255))      # headlight
    d.rectangle((2, 18, 3, 19), fill=(200, 30, 30, 255))          # tail light
    for cx in (8, 23):                                            # wheels
        d.ellipse((cx - 4, 19, cx + 4, 27), fill=(12, 12, 14, 255))
        d.ellipse((cx - 2, 21, cx + 2, 25), fill=(150, 150, 160, 255))
    return im


def phone():
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 2, 23, 29), radius=3, fill=(22, 22, 28, 255))          # body
    d.rounded_rectangle((8, 2, 23, 29), radius=3, outline=(240, 200, 60, 255))     # gold rim
    d.rectangle((10, 5, 21, 25), fill=(20, 110, 140, 255))                          # screen
    for y in range(5, 26):                                                          # screen gradient
        c = (20 + (y - 5) * 2, 110 + (y - 5) * 3, 150 + (y - 5) * 3, 255)
        d.line((10, y, 21, y), fill=c)
    d.rectangle((14, 3, 17, 3), fill=(60, 60, 70, 255))                             # notch / speaker
    cols = [(240, 200, 60, 255), (60, 220, 230, 255), (230, 90, 150, 255), (120, 220, 90, 255)]
    for r in range(3):                                                              # app icons
        for c in range(3):
            x, y = 11 + c * 4, 8 + r * 5
            d.rectangle((x, y, x + 2, y + 2), fill=cols[(r * 3 + c) % 4])
    d.rectangle((14, 27, 17, 27), fill=(150, 150, 160, 255))                        # home bar
    return im


def build(pack):
    tex = os.path.join(pack, 'assets/mcdistrict/textures/item')
    mod = os.path.join(pack, 'assets/mcdistrict/models/item')
    itm = os.path.join(pack, 'assets/mcdistrict/items')
    squid().save(os.path.join(tex, 'icon_squid.png'))
    copcar().save(os.path.join(tex, 'icon_copcar.png'))
    phone().save(os.path.join(tex, 'icon_phone.png'))
    shutil.copy(os.path.join(HERE, 'icon_anarchy_src.png'), os.path.join(tex, 'icon_anarchy.png'))
    for n in ('icon_squid', 'icon_copcar', 'icon_anarchy', 'icon_phone'):
        json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'mcdistrict:item/' + n}},
                  open(os.path.join(mod, n + '.json'), 'w'), indent=1)
        json.dump({'model': {'type': 'minecraft:model', 'model': 'mcdistrict:item/' + n}},
                  open(os.path.join(itm, n + '.json'), 'w'), indent=1)
    # big preview of the three for checking by eye
    sheet = Image.new('RGBA', (3 * 256 + 40, 296), (36, 38, 46, 255))
    for i, n in enumerate(('icon_squid', 'icon_copcar', 'icon_anarchy')):
        sheet.paste(Image.open(os.path.join(tex, n + '.png')).convert('RGBA').resize((256, 256), Image.NEAREST), (10 + i * 266, 20))
    sheet.save(os.path.join(HERE, 'icons_preview.png'))
