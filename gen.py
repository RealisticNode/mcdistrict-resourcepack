# MCDistrict Gun Fight resource pack: 8 block-built 3D gun models (Java item models), one palette texture,
# item model definitions for the item_model component (mcdistrict:<gun>), plus side/top preview renders.
import json, os, zipfile, hashlib, random
from PIL import Image, ImageDraw

OUT = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(OUT, 'pack')

# palette swatches (8 x 8 px each in a 64 x 64 texture)
PAL = {
    'metal': (58, 61, 66), 'black': (30, 31, 34), 'dark': (78, 82, 88), 'steel': (128, 134, 142),
    'wood': (112, 70, 38), 'lwood': (150, 100, 56), 'olive': (75, 83, 40), 'tan': (170, 146, 104),
    'red': (190, 50, 40), 'glass': (90, 160, 200), 'brass': (181, 137, 59), 'rubber': (22, 22, 24),
    'paint': (236, 236, 236),  # body parts: tinted by the item (default colour or the player's skin)
}

# the body material of each gun: those parts get repainted by skins
MAIN = {'pistol': 'metal', 'revolver': 'metal', 'smg': 'black', 'shotgun': 'metal', 'rifle': 'black',
        'marksman': 'tan', 'sniper': 'metal', 'lmg': 'olive'}
KEYS = list(PAL)


def texture():
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    rnd = random.Random(7)
    for k, name in enumerate(KEYS):
        c, r = k % 8, k // 8
        base = PAL[name]
        for x in range(8):
            for y in range(8):
                n = rnd.randint(-7, 7)
                edge = -14 if x in (0, 7) or y in (0, 7) else 0
                img.putpixel((c * 8 + x, r * 8 + y), tuple(max(0, min(255, v + n + edge)) for v in base) + (255,))
    return img


def uv(name):
    k = KEYS.index(name)
    c, r = k % 8, k // 8
    return [c * 2 + 0.3, r * 2 + 0.3, c * 2 + 1.7, r * 2 + 1.7]


def box(x1, y1, z1, x2, y2, z2, mat):
    return (x1, y1, z1, x2, y2, z2, mat)


Z0, Z1 = 7, 9  # default body width (2 units, centred on z = 8)


def guns():
    g = {}
    g['pistol'] = [
        box(3, 8, Z0, 13, 10.5, Z1, 'metal'),          # slide
        box(3, 7, 7.2, 12, 8, 8.8, 'black'),           # frame
        box(12.6, 8.6, 7.6, 13.4, 9.6, 8.4, 'black'),  # muzzle
        box(3.2, 2.5, 7.1, 6, 7, 8.9, 'black'),        # grip
        box(6, 5.4, 7.6, 8.6, 5.9, 8.4, 'black'),      # trigger guard
        box(8.1, 5.9, 7.6, 8.6, 7, 8.4, 'black'),
        box(6.6, 6, 7.8, 7, 7, 8.2, 'steel'),          # trigger
        box(11.5, 10.5, 7.7, 12.3, 11, 8.3, 'black'),  # front sight
        box(3.4, 10.5, 7.5, 4.4, 11, 8.5, 'black'),    # rear sight
    ]
    g['revolver'] = [
        box(9, 8.6, 7.4, 17, 9.8, 8.6, 'steel'),       # barrel
        box(9, 8.3, 7.6, 16, 8.6, 8.4, 'steel'),       # ejector rod
        box(6, 7.4, 6.6, 9, 10.2, 9.4, 'steel'),       # cylinder
        box(4.5, 7, 7.2, 9.2, 10.6, 8.8, 'metal'),     # frame
        box(2.8, 2.5, 7, 5.6, 7.4, 9, 'wood'),         # grip
        box(4, 10.4, 7.6, 5, 11.4, 8.4, 'metal'),      # hammer
        box(5.6, 5.6, 7.6, 8, 6.1, 8.4, 'metal'),      # trigger guard
        box(16, 9.8, 7.7, 16.6, 10.5, 8.3, 'metal'),   # front sight
    ]
    g['smg'] = [
        box(2, 7, Z0, 14, 10, Z1, 'black'),            # receiver
        box(14, 8, 7.5, 18, 9, 8.5, 'metal'),          # barrel
        box(13, 7.5, 7.2, 15, 9.5, 8.8, 'dark'),       # barrel collar
        box(8, 1.5, 7.3, 10, 7, 8.7, 'black'),         # magazine
        box(3, 3.5, 7.2, 5.2, 7, 8.8, 'rubber'),       # grip
        box(5.2, 5.6, 7.6, 7.8, 6.1, 8.4, 'black'),    # trigger guard
        box(-3, 8, 7.6, 2, 9, 8.4, 'metal'),           # folded stock
        box(-3.5, 6.5, 7.4, -2.5, 9, 8.6, 'black'),    # stock butt
        box(9, 10, 7.6, 12, 10.6, 8.4, 'black'),       # rail
        box(13, 10, 7.7, 13.6, 10.8, 8.3, 'black'),    # front sight
    ]
    g['shotgun'] = [
        box(4, 8.8, 7.4, 24, 9.8, 8.6, 'steel'),       # barrel
        box(6, 7.8, 7.5, 22, 8.8, 8.5, 'metal'),       # magazine tube
        box(12, 7.4, 6.8, 18, 9.2, 9.2, 'wood'),       # pump
        box(-1, 7.4, 7, 6, 10.2, 9, 'metal'),          # receiver
        box(-9, 5.6, 7.2, -1, 9.6, 8.8, 'wood'),       # stock
        box(-10, 4.8, 7.1, -9, 9.4, 8.9, 'rubber'),    # butt pad
        box(1, 5.8, 7.6, 3.6, 6.3, 8.4, 'metal'),      # trigger guard
        box(23, 9.8, 7.8, 23.6, 10.4, 8.2, 'brass'),   # bead sight
    ]
    g['rifle'] = [
        box(0, 7, Z0, 12, 10.5, Z1, 'black'),          # receiver
        box(12, 7.5, 6.8, 20, 10, 9.2, 'black'),       # handguard
        box(20, 8.3, 7.5, 25, 9.2, 8.5, 'metal'),      # barrel
        box(24, 8, 7.3, 25.6, 9.5, 8.7, 'dark'),       # muzzle brake
        box(7, 2, 7.2, 9.6, 7, 8.8, 'black'),          # magazine
        box(7.6, 1, 7.2, 10.2, 2.2, 8.8, 'black'),     # mag curve
        box(2, 3, 7.2, 4.2, 7, 8.8, 'rubber'),         # grip
        box(4.2, 5.6, 7.6, 6.8, 6.1, 8.4, 'black'),    # trigger guard
        box(-8, 6.5, 7.2, 0, 10, 8.8, 'black'),        # stock
        box(-9, 5.5, 7.1, -8, 10.3, 8.9, 'rubber'),    # butt pad
        box(1, 10.5, 7.5, 18, 11, 8.5, 'metal'),       # top rail
        box(3, 11, 7.6, 5, 12.2, 8.4, 'black'),        # rear sight
        box(18, 10, 7.7, 19, 12, 8.3, 'black'),        # front sight post
    ]
    g['marksman'] = [
        box(0, 7, Z0, 13, 10.4, Z1, 'tan'),            # receiver
        box(13, 7.4, 6.9, 21, 9.9, 9.1, 'tan'),        # handguard
        box(21, 8.3, 7.5, 28, 9.1, 8.5, 'metal'),      # barrel
        box(27.4, 8, 7.3, 28.8, 9.4, 8.7, 'black'),    # muzzle
        box(7.5, 2.5, 7.3, 9.8, 7, 8.7, 'black'),      # magazine
        box(2, 3, 7.2, 4.2, 7, 8.8, 'black'),          # grip
        box(4.2, 5.6, 7.6, 6.8, 6.1, 8.4, 'black'),    # trigger guard
        box(-9, 6.2, 7.2, 0, 10, 8.8, 'tan'),          # stock
        box(-6, 10, 7.4, -1, 10.8, 8.6, 'black'),      # cheek rest
        box(1, 10.4, 7.5, 19, 10.9, 8.5, 'black'),     # rail
        box(3, 11.4, 7.1, 13, 12.9, 8.9, 'black'),     # scope tube
        box(1.5, 11.1, 6.8, 3, 13.2, 9.2, 'black'),    # eyepiece
        box(13, 11, 6.7, 14.6, 13.4, 9.3, 'black'),    # objective
        box(14.5, 11.3, 7.1, 14.7, 13.1, 8.9, 'glass'),# lens
        box(6, 10.9, 7.6, 8, 11.4, 8.4, 'black'),      # mount
    ]
    g['sniper'] = [
        box(-10, 5.8, 7.1, 2, 9.8, 8.9, 'wood'),       # stock
        box(-11, 5, 7, -10, 9.6, 9, 'rubber'),         # butt pad
        box(-7, 9.8, 7.3, -1, 10.6, 8.7, 'wood'),      # cheek rest
        box(-1, 3, 7.2, 1.2, 6.5, 8.8, 'wood'),        # grip
        box(2, 7.2, 7, 11, 10, 9, 'metal'),            # receiver
        box(11, 7.6, 7.1, 18, 9.6, 8.9, 'wood'),       # fore-end
        box(11, 8.4, 7.55, 31, 9.2, 8.45, 'metal'),    # barrel
        box(30.4, 8.1, 7.3, 31.8, 9.5, 8.7, 'black'),  # muzzle
        box(6, 8.2, 9, 6.8, 9, 10.6, 'steel'),         # bolt handle
        box(6, 8, 10.4, 6.8, 9.2, 11, 'steel'),        # bolt knob
        box(2.2, 5.6, 7.6, 4.6, 6.1, 8.4, 'metal'),    # trigger guard
        box(1, 11.2, 7.05, 14, 13, 8.95, 'black'),     # scope tube
        box(-0.6, 10.9, 6.7, 1.2, 13.3, 9.3, 'black'), # eyepiece
        box(14, 10.7, 6.5, 16, 13.5, 9.5, 'black'),    # objective
        box(15.9, 11, 6.8, 16.1, 13.2, 9.2, 'glass'),  # lens
        box(4, 10, 7.6, 5, 11.2, 8.4, 'black'),        # mount
        box(10, 10, 7.6, 11, 11.2, 8.4, 'black'),      # mount
        box(7, 13, 7.6, 8, 13.6, 8.4, 'black'),        # turret
        box(16.5, 4, 6.4, 17.1, 8, 7, 'metal'),        # bipod leg
        box(16.5, 4, 9, 17.1, 8, 9.6, 'metal'),        # bipod leg
    ]
    g['lmg'] = [
        box(0, 6.5, 6.6, 14, 11, 9.4, 'olive'),        # receiver
        box(14, 7.4, 6.8, 21, 10.4, 9.2, 'black'),     # heat shroud
        box(21, 8.3, 7.5, 28, 9.3, 8.5, 'metal'),      # barrel
        box(27.4, 8, 7.3, 28.8, 9.6, 8.7, 'black'),    # flash hider
        box(5, 1.5, 4.8, 11, 6.5, 6.8, 'olive'),       # box magazine (left side)
        box(6, 6.5, 5.5, 9, 7.5, 6.6, 'black'),        # feed
        box(1.5, 2.8, 7.2, 3.8, 6.5, 8.8, 'rubber'),   # grip
        box(3.8, 5.5, 7.6, 6.4, 6, 8.4, 'black'),      # trigger guard
        box(-9, 6.5, 7.1, 0, 10.5, 8.9, 'black'),      # stock
        box(-10, 5.6, 7, -9, 10.8, 9, 'rubber'),       # butt pad
        box(4, 11, 7.5, 12, 11.5, 8.5, 'black'),       # rail
        box(7, 11.5, 7.7, 8, 13, 8.3, 'black'),        # carry handle post
        box(7, 12.8, 7.7, 12, 13.4, 8.3, 'black'),     # carry handle
        box(11, 11.5, 7.7, 12, 13, 8.3, 'black'),
        box(19, 3.5, 6.2, 19.6, 7.4, 6.8, 'metal'),    # bipod
        box(19, 3.5, 9.2, 19.6, 7.4, 9.8, 'metal'),
        box(20, 10.4, 7.7, 20.8, 11.6, 8.3, 'black'),  # front sight
    ]
    return g


def center(boxes):
    """shift the gun so its bounding box is centred on (8, 8, 8): the display rotations pivot there"""
    xs = [b[0] for b in boxes] + [b[3] for b in boxes]
    ys = [b[1] for b in boxes] + [b[4] for b in boxes]
    dx = 8 - (min(xs) + max(xs)) / 2
    dy = 8 - (min(ys) + max(ys)) / 2
    return [(b[0] + dx, b[1] + dy, b[2], b[3] + dx, b[4] + dy, b[5], b[6]) for b in boxes], max(xs) - min(xs)


def model(boxes, length, main):
    elems = []
    for b in boxes:
        paint = b[6] == main
        f = {face: dict({'uv': uv('paint' if paint else b[6]), 'texture': '#0'}, **({'tintindex': 0} if paint else {}))
             for face in ('north', 'east', 'south', 'west', 'up', 'down')}
        elems.append({'from': [round(b[0], 3), round(b[1], 3), round(b[2], 3)], 'to': [round(b[3], 3), round(b[4], 3), round(b[5], 3)], 'faces': f})
    s = 16 / max(16, length)  # fit long guns in the GUI slot
    return {
        'credit': 'MCDistrict Gun Fight - RealisticNode',
        'texture_size': [64, 64],
        'textures': {'0': 'mcdistrict:item/guns', 'particle': 'mcdistrict:item/guns'},
        'elements': elems,
        'display': {
            'thirdperson_righthand': {'rotation': [0, -90, 0], 'translation': [0, 3, 1.5], 'scale': [0.55, 0.55, 0.55]},
            'thirdperson_lefthand': {'rotation': [0, 90, 0], 'translation': [0, 3, 1.5], 'scale': [0.55, 0.55, 0.55]},
            'firstperson_righthand': {'rotation': [0, -90, 0], 'translation': [3, 3.5, -2], 'scale': [0.65, 0.65, 0.65]},
            'firstperson_lefthand': {'rotation': [0, 90, 0], 'translation': [3, 3.5, -2], 'scale': [0.65, 0.65, 0.65]},
            'gui': {'rotation': [15, -30, 0], 'translation': [0, 0, 0], 'scale': [round(0.9 * s, 3)] * 3},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.4, 0.4, 0.4]},
            'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [round(0.9 * s, 3)] * 3},
            'head': {'rotation': [0, 0, 0], 'translation': [0, 12, 0], 'scale': [0.6, 0.6, 0.6]},
        },
    }


def shield_model(blocking):
    """riot shield: tall dark panel with a viewing window, a white stripe and a handle on the back"""
    bx = [
        box(2, -3, 7, 14, 19, 8, 'black'),           # panel
        box(1.6, -3.4, 6.8, 14.4, -3, 8.2, 'dark'),  # rim
        box(1.6, 19, 6.8, 14.4, 19.4, 8.2, 'dark'),
        box(1.6, -3, 6.8, 2, 19, 8.2, 'dark'),
        box(14, -3, 6.8, 14.4, 19, 8.2, 'dark'),
        box(4, 11, 6.9, 12, 15, 7.1, 'glass'),       # window
        box(2, 5, 6.9, 14, 6.4, 7.1, 'steel'),       # stripe
        box(6, 6.5, 8, 10, 7.5, 9.6, 'metal'),       # handle
        box(6, 6.5, 9.6, 10, 7.5, 9.8, 'rubber'),
    ]
    elems = [{'from': [b[0], b[1], b[2]], 'to': [b[3], b[4], b[5]],
              'faces': {f: {'uv': uv(b[6]), 'texture': '#0'} for f in ('north', 'east', 'south', 'west', 'up', 'down')}} for b in bx]
    disp = {
        'thirdperson_righthand': {'rotation': [0, 90, 0], 'translation': [10, 6, -4], 'scale': [1, 1, 1]},
        'thirdperson_lefthand': {'rotation': [0, 90, 0], 'translation': [10, 6, 12], 'scale': [1, 1, 1]},
        'firstperson_righthand': {'rotation': [0, 180, 5], 'translation': [-10, 2, -10], 'scale': [1.25, 1.25, 1.25]},
        'firstperson_lefthand': {'rotation': [0, 180, 5], 'translation': [10, 0, -10], 'scale': [1.25, 1.25, 1.25]},
        'gui': {'rotation': [15, -25, -5], 'translation': [2, 3, 0], 'scale': [0.65, 0.65, 0.65]},
        'fixed': {'rotation': [0, 180, 0], 'translation': [-2, 4, -5], 'scale': [0.5, 0.5, 0.5]},
        'ground': {'rotation': [0, 0, 0], 'translation': [4, 4, 2], 'scale': [0.25, 0.25, 0.25]},
    }
    if blocking:
        disp['thirdperson_righthand'] = {'rotation': [45, 135, 0], 'translation': [3.51, 11, -2], 'scale': [1, 1, 1]}
        disp['thirdperson_lefthand'] = {'rotation': [45, 135, 0], 'translation': [13.51, 3, 5], 'scale': [1, 1, 1]}
        disp['firstperson_righthand'] = {'rotation': [0, 180, -5], 'translation': [-15, 5, -11], 'scale': [1.25, 1.25, 1.25]}
        disp['firstperson_lefthand'] = {'rotation': [0, 180, -5], 'translation': [5, 5, -11], 'scale': [1.25, 1.25, 1.25]}
    return {'credit': 'MCDistrict Gun Fight - RealisticNode', 'texture_size': [64, 64],
            'textures': {'0': 'mcdistrict:item/guns', 'particle': 'mcdistrict:item/guns'}, 'elements': elems, 'display': disp}


def preview(name, boxes, path):
    """side view (x/y) above top view (x/z), painter-sorted, 12 px per unit"""
    S, pad = 12, 10
    xs = [b[0] for b in boxes] + [b[3] for b in boxes]
    W = int((max(xs) - min(xs)) * S) + 2 * pad
    img = Image.new('RGB', (W, 16 * S + 6 * S + 3 * pad), (32, 34, 40))
    d = ImageDraw.Draw(img)
    x0 = min(xs)
    for b in sorted(boxes, key=lambda b: b[5]):
        c = PAL[b[6]]
        d.rectangle([pad + (b[0] - x0) * S, pad + (16 - b[4]) * S, pad + (b[3] - x0) * S, pad + (16 - b[1]) * S], fill=c, outline=tuple(max(0, v - 25) for v in c))
    oy = 16 * S + 2 * pad
    for b in sorted(boxes, key=lambda b: b[4]):
        c = tuple(min(255, v + 18) for v in PAL[b[6]])
        d.rectangle([pad + (b[0] - x0) * S, oy + (b[2] - 5) * S, pad + (b[3] - x0) * S, oy + (b[5] - 5) * S], fill=c, outline=tuple(max(0, v - 25) for v in c))
    d.text((pad, 2), name, fill=(220, 220, 220))
    img.save(path)


def main():
    tex_dir = os.path.join(PACK, 'assets/mcdistrict/textures/item')
    mod_dir = os.path.join(PACK, 'assets/mcdistrict/models/item')
    item_dir = os.path.join(PACK, 'assets/mcdistrict/items')
    for p in (tex_dir, mod_dir, item_dir, os.path.join(OUT, 'preview')):
        os.makedirs(p, exist_ok=True)
    texture().save(os.path.join(tex_dir, 'guns.png'))
    for name, boxes in guns().items():
        boxes, length = center(boxes)
        json.dump(model(boxes, length, MAIN[name]), open(os.path.join(mod_dir, name + '.json'), 'w'), indent=1)
        r, g_, b_ = (min(255, round(v * 255 / 236)) for v in PAL[MAIN[name]])
        json.dump({'model': {'type': 'minecraft:model', 'model': 'mcdistrict:item/' + name,
                             'tints': [{'type': 'minecraft:custom_model_data', 'index': 0, 'default': (r << 16) | (g_ << 8) | b_}]}},
                  open(os.path.join(item_dir, name + '.json'), 'w'), indent=1)
        preview(name, boxes, os.path.join(OUT, 'preview', name + '.png'))
    json.dump(shield_model(False), open(os.path.join(mod_dir, 'riot_shield.json'), 'w'), indent=1)
    json.dump(shield_model(True), open(os.path.join(mod_dir, 'riot_shield_blocking.json'), 'w'), indent=1)
    json.dump({'model': {'type': 'minecraft:condition', 'property': 'minecraft:using_item',
                         'on_true': {'type': 'minecraft:model', 'model': 'mcdistrict:item/riot_shield_blocking'},
                         'on_false': {'type': 'minecraft:model', 'model': 'mcdistrict:item/riot_shield'}}},
              open(os.path.join(item_dir, 'riot_shield.json'), 'w'), indent=1)
    json.dump({'pack': {'description': 'MCDistrict Gun Fight weapons', 'pack_format': 46,
                        'supported_formats': {'min_inclusive': 46, 'max_inclusive': 999},
                        'min_format': 46, 'max_format': 999}}, open(os.path.join(PACK, 'pack.mcmeta'), 'w'), indent=1)
    zpath = os.path.join(OUT, 'mcd-guns.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(PACK):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, PACK).replace(os.sep, '/'))
    sha1 = hashlib.sha1(open(zpath, 'rb').read()).hexdigest()
    print('zip', os.path.getsize(zpath), 'bytes sha1', sha1)


main()
