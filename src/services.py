import io
from typing import List

from aiogram import types
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import config as cfg


async def get_results_list(message: types.Message = None,
        user: types.User = None) -> List[types.InputMediaPhoto]:
    source = await _download_image(message=message, user=user)

    results = []
    i = 0
    while True:
        path = 'logos/{}.png'.format(str(i))
        try:
            result = _paste_mask(Image.open(path), source)
            response = io.BytesIO()
            response.name = "response.png"
            result.save(response, 'PNG')
            response.seek(0)
            if i == 0:
                caption = cfg.CAPTION
            else:
                caption = None
            res = types.InputMediaPhoto(response, caption=caption)
            results.append(res)
            i += 1
        except FileNotFoundError:
            break
    return results


async def _download_image(message: types.Message = None,
        user: types.User = None) -> Image:
    if message:
        return await _download_image_from_message(message)
    if user:
        return await _download_user_profile_image(user)
    else:
        class SourceNotFound(Exception):
            pass
        raise SourceNotFound('Not found source for download image.')


async def _download_image_from_message(message: types.Message) -> Image:
    return Image.open(await message.photo[-1].download(io.BytesIO()))\
        .convert('RGBA')


async def _download_user_profile_image(user: types.User) -> Image:
    photos = await user.get_profile_photos(limit=1)
    return Image.open(await photos.photos[0][-1].download(io.BytesIO()))\
        .convert('RGBA')


def _paste_mask(logo: Image, source: Image) -> Image:
    h, w = source.size
    min_dim = min(h, w)
    
    logo = logo.resize((min_dim, min_dim))
    delta_x = h - min_dim
    delta_y = w - min_dim
    logo = ImageOps.expand(logo, (
            delta_x // 2 + (1 if delta_x % 2 == 1 else 0),
            delta_y // 2 + (1 if delta_y % 2 == 1 else 0),
            delta_x // 2, delta_y // 2))

    alpha = ImageEnhance.Brightness(logo.split()[3]).enhance(1)
    logo.putalpha(alpha)
    return Image.alpha_composite(source, logo)
