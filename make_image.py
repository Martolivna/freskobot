from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

base = Image.open("template.png").convert("RGBA")


def make_image(question, time):
    img = _make_image(question, time)
    iob = BytesIO()
    img.save(iob, format='png')
    return iob.getvalue()


def _make_image(question, time):
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    d.text((20, 16), "Загадка от Жака Фреско", font=fnt(32), fill=(255, 255, 255))
    d.text((50, 125), f"{question}\nСколько?", font=fnt(52), fill=(255, 255, 255), align='center')
    d.text((10, 325), f"На размышление дается \n{time} секунд", font=fnt(25), fill=(255, 255, 255))
    out = Image.alpha_composite(base, txt)
    return out


def fnt(size):
    return ImageFont.truetype("SourceCodePro-Medium", size)


if __name__ == "__main__":
    _make_image("2+3", 60).show()
