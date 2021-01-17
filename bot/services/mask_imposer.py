from io import BytesIO
from PIL import Image, ImageEnhance, ImageOps
from queue import Queue
from threading import Thread

from config import MASK_ENHANCE as ENHANCE


class MaskImposer(Thread):
    def __init__(self, path: str, number: int, source: Image, queue: Queue):
        Thread.__init__(self)
        self._mask = Image.open(path.format(number))
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
        alpha = ImageEnhance.Brightness(mask.split()[3]).enhance(ENHANCE)
        mask.putalpha(alpha)

        # impose mask to image as alpha layer and return result
        self._image = Image.alpha_composite(self._source, mask)
        return self._image
