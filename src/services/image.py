from PIL import Image, ImageDraw, ImageFont


def set_text(num: str, text: str):
    image = Image.open("data/orig.png")
    draw = ImageDraw.Draw(image)
    font_num = ImageFont.truetype("data/font.ttf", 133)
    w, h = draw.textsize(num, font=font_num)
    font_t = ImageFont.truetype("data/font.ttf", 75)
    draw.text(
        ((image.width-w)/2 + 605,(image.height-h)/2 - 70),
        num,
        fill="white",
        font=font_num,
    )
    if len(text) == 3:
        draw.text((1495, 543), text, fill="white", font=font_t, align="center")
    else:
        draw.text((1467, 543), text, fill="white", font=font_t, align="center")

    image.save(f"images/{num}.png")
    return f"images/{num}.png"


def _debug_set_text(num, text, p_x, p_y):
    image = Image.open("src/data/orig.png")
    draw = ImageDraw.Draw(image)
    font_num = ImageFont.truetype("src/data/font.ttf", 133)
    w, h = draw.textsize(num, font=font_num)
    font_t = ImageFont.truetype("src/data/font.ttf", 75)
    draw.text(
        ((image.width-w)/2 + p_x,(image.height-h)/2 + p_y),
        num,
        fill="white",
        font=font_num,
    )
    if len(text) == 3:
        draw.text((1495, 543), text, fill="white", font=font_t, align="center")
    else:
        draw.text((1467, 543), text, fill="white", font=font_t, align="center")

    image.show()
