from PIL import ImageOps, Image
from cairosvg import svg2png
from io import BytesIO


def frame(im, thickness=5):
    iw, ih = im.size
    ow, oh = iw + 2 * thickness, ih + 2 * thickness

    outer = f'<svg width="{ow}" height="{oh}" style="background-color:none"><rect rx="15" ry="20" width="{ow}"' \
            f' height="{oh}" fill="black"/></svg>'
    png = svg2png(bytestring=outer)
    outer = Image.open(BytesIO(png))

    inner = f'<svg width="{ow}" height="{oh}"><rect x="{thickness}" y="{thickness}" rx="15" ry="20" width="{iw}"' \
            f' height="{ih}" fill="white"/></svg>'
    png = svg2png(bytestring=inner)
    inner = Image.open(BytesIO(png)).convert('L')

    expanded = ImageOps.expand(im, border=thickness, fill=(0, 0, 0)).convert('RGB')

    outer.paste(expanded, None, inner)
    return outer


def round_apply(filename):
    im = Image.open(filename)
    result = frame(im, thickness=5)
    new_image = 'result.png'
    result.save(new_image)
    return new_image
