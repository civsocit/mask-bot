"""
Module for downloading image from Telegram message or user profile.
"""
import io
from typing import Union

from aiogram import types
from PIL import Image


async def download_image(obj: Union[types.Message, types.User]) -> Image:
    """Main download function."""
    if isinstance(obj, types.Message):
        return await _download_image_from_message(obj)
    if isinstance(obj, types.User):
        return await _download_user_profile_image(obj)
    else:
        raise SourceNotFound('Not found source for download image.')


async def _download_image_from_message(message: types.Message) -> Image:
    # download image from message as bytes string
    image = await message.photo[-1].download(io.BytesIO())
    return Image.open(image).convert('RGBA')


async def _download_user_profile_image(user: types.User) -> Image:
    # get list of lists with user profile photo
    photos = await user.get_profile_photos(limit=1)
    # download image as bytes string
    image = await photos.photos[0][-1].download(io.BytesIO())
    return Image.open(image).convert('RGBA')


class SourceNotFound(Exception):
    pass
