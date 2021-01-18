import logging
import os
from datetime import datetime
from io import BytesIO
from queue import Queue
from threading import Thread
from typing import List, Union

from aiogram import types
from PIL import Image, ImageEnhance, ImageOps

from bot.services import download_image


async def impose_masks(
    obj: Union[types.Message, types.User]
) -> List[types.InputMediaPhoto]:
    """Impose all masks to source image."""
    # starting time
    start = datetime.now()

    # download source image
    source = await download_image(obj)

    # count of masks in the folder
    i = 0
    while True:
        if os.path.exists(obj.bot.config.MASKS_PATH.format(str(i))):
            i += 1
        else:
            break

    # queue for memorize results
    queue = Queue(i + 1)

    # create workers
    workers = [MaskImposer(obj.bot.config.MASKS_PATH,
                           n,
                           obj.bot.config.MASK_ENHANCE,
                           source,
                           queue) for n in range(i)]

    for w in workers:
        w.start()

    for w in workers:
        w.join()

    # add InputMediaPhoto results to list
    results = []
    while queue.qsize():
        results.append(types.InputMediaPhoto(queue.get()))

    # set caption for first image
    results[0].caption = obj.bot.config.CAPTION

    logging.info('Images generation time: {}.'.format(datetime.now() - start))

    return results


class MaskImposer(Thread):
    def __init__(self,
                 path: str,
                 number: int,
                 mask_enhance: int,
                 source: Image,
                 queue: Queue):
        Thread.__init__(self)
        self._mask = Image.open(path.format(number))
        self._mask_enhance = mask_enhance
        self._source = source
        self._queue = queue

    def run(self):
        """Put result to queue as bytes string."""
        result = self._impose_mask()
        response = BytesIO()
        response.name = 'response.png'
        result.save(response, 'PNG')
        response.seek(0)
        self._queue.put(response)

    def _impose_mask(self) -> Image:
        """Impose mask to Image object."""
        # get min source size
        h, w = self._source.size
        min_dim = min(h, w)

        # resize mask to min source size
        mask = self._mask.resize((min_dim, min_dim))

        # add transperent border to mask for correct impose
        delta_x = h - min_dim
        delta_y = w - min_dim
        mask = ImageOps.expand(mask, (
                delta_x // 2 + (1 if delta_x % 2 == 1 else 0),
                delta_y // 2 + (1 if delta_y % 2 == 1 else 0),
                delta_x // 2, delta_y // 2))

        # convert image to RGB and setting brightness
        alpha = ImageEnhance.Brightness(
            mask.split()[3]
        ).enhance(self._mask_enhance)
        mask.putalpha(alpha)

        # impose mask to image as alpha layer and return result
        self._image = Image.alpha_composite(self._source, mask)
        return self._image
