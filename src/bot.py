import io

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from PIL import Image

import config as cfg
from services import get_results_list


bot = Bot(cfg.TOKEN, parse_mode='html')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer(cfg.TEXT)


@dp.message_handler(commands=['profile'])
async def from_profile(message: types.Message):
    await message.answer_media_group(await get_results_list(user=message\
        .from_user))


@dp.message_handler(content_types=ContentType.PHOTO)
async def from_photo(message: types.Message):
    await message.answer_media_group(await get_results_list(message=message))


async def on_startup(dp: Dispatcher):
    await dp.bot.set_my_commands([
            types.BotCommand('profile',
                             'сгенерировать картинку из нынешнего аватара'),
            types.BotCommand('help', 'информация о том, как работает бот')])


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
