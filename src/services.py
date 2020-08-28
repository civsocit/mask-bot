import datetime
import io
import os
import threading
from typing import List
import queue

from aiogram import types
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

import config as cfg
from exceptions import SourceNotFound


async def get_results_list(message: types.Message = None,
        user: types.User = None) -> List[types.InputMediaPhoto]:
    start = datetime.datetime.now()

    source = await _download_image(message=message, user=user)
    path = 'masks/{}.png'

    i = 0
    while True:
        if os.path.exists(path.format(str(i))):
            i += 1
        else:
            break
    
    t_results = queue.Queue(i + 1)
    
    workers = [threading.Thread(target=_paste_mask_worker, args=(path, n, source, t_results)) for n in range(i)]
    
    for w in workers:
        w.start()
    
    for w in workers:
        w.join()
    
    results = []
    while t_results.qsize():
        results.append(types.InputMediaPhoto(t_results.get()))

    results[0].caption = cfg.CAPTION
    
    end = datetime.datetime.now()
    return [results, (end - start)]


async def _download_image(message: types.Message = None,
        user: types.User = None) -> Image:
    if message:
        return await _download_image_from_message(message)
    if user:
        return await _download_user_profile_image(user)
    else:
        raise SourceNotFound('Not found source for download image.')


async def _download_image_from_message(message: types.Message) -> Image:
    return Image.open(await message.photo[-1].download(io.BytesIO()))\
        .convert('RGBA')


async def _download_user_profile_image(user: types.User) -> Image:
    photos = await user.get_profile_photos(limit=1)
    image = await photos.photos[0][-1].download(io.BytesIO())
    return Image.open(image).convert('RGBA')


def _paste_mask_worker(path, number, source, results):
    result = _paste_mask(Image.open(path.format(number)), source)
    response = io.BytesIO()
    response.name = "response.png"
    result.save(response, 'PNG')
    response.seek(0)
    results.put(response)


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
