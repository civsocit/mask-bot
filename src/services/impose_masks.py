from datetime import datetime
import logging
import os
from queue import Queue
from typing import List

from aiogram import types

from config import CAPTION, MASKS_PATH as PATH
from .downloader import download_image
from .mask_imposer import MaskImposer


async def impose_masks(message: types.Message = None,
        user: types.User = None) -> List[types.InputMediaPhoto]:
    """Impose all masks to source image."""
    # starting time
    start = datetime.now()

    # download source image
    source = await download_image(message=message, user=user)

    # count of masks in the folder
    i = 0
    while True:
        if os.path.exists(PATH.format(str(i))):
            i += 1
        else:
            break
    
    # queue for memorize results
    queue = Queue(i + 1)

    # create workers
    workers = [MaskImposer(PATH, n, source, queue) for n in range(i)]

    for w in workers:
        w.start()
    
    for w in workers:
        w.join()
    
    # add InputMediaPhoto results to list
    results = []
    while queue.qsize():
        results.append(types.InputMediaPhoto(queue.get()))
    
    # set caption for first image
    results[0].caption = CAPTION

    logging.info('Images generation time: {}.'.format(datetime.now() - start))

    return results
